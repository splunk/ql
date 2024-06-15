require([
    "splunkjs/mvc",
    "splunkjs/mvc/simplexml/ready!",
    'jquery'
], function(
    mvc
) {
    var defaultTokenModel = mvc.Components.get("default");
    defaultTokenModel.on("change:access", function(newAccessValue, access, options) {
        if (access === "false") {
            $('#fieldset1').find('input, textarea, button, select').prop('disabled', true).prop('style', 'pointer-events: none');
        }
    });

    // token onChange event for soar_cases_performance.xml view sometimes not picked up by handler on page reload
    var tokenAccess = defaultTokenModel.get("access");
    if (tokenAccess === "false") {
        $('#fieldset1').find('input, textarea, button, select').prop('disabled', true).prop('style', 'pointer-events: none');
    }
});
