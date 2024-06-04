__non_webpack_require__([
    "underscore",
    "backbone",
    "splunkjs/mvc",
    "jquery",
], function(
    _,
    Backbone,
    mvc,
    $
){

    require(["@splunk/swc-lookup/collections/SplunkDsBase",], function(SplunkDsBaseCollection) {

        var KVLookups = SplunkDsBaseCollection.extend({
            url: '/splunkd/__raw/servicesNS/nobody/lookup_editor/storage/collections/config?count=-1',
            initialize: function() {
              SplunkDsBaseCollection.prototype.initialize.apply(this, arguments);
            }
        });
        
        kv_lookups = new KVLookups();
        
        kv_lookups.fetch({
            complete: function(jqXHR, textStatus){
                if( jqXHR.status == 404){
                    $(".show-kv-supported-only").hide();
                    $(".show-kv-unsupported-only").show();
                }
            }.bind(this)
        });

    })
	
	
	
});