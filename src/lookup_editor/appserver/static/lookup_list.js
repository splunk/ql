__non_webpack_require__([
         "jquery",
         "underscore",
         "backbone",
         "splunkjs/mvc/simplexml/ready!",
     ], function(
         $,
         _,
         Backbone,
     )
     {

        require(['lookup-static/js/views/LookupListView'], function(LookupListView){
            /**
             * Everything is being managed from xml & LookupListView
             */
    
            // var lookupListView = new LookupListView({
            //     el: $('#lookups_list')
            // });
            // lookupListView.render();
        })
     }
);