import Template from "lookup-static/js/templates/KVStoreFieldView.html"
import SimpleSplunkView from "splunkjs/mvc/simplesplunkview";
import "../../css/KVStoreFieldView.css"

    var KVStoreFieldView = SimpleSplunkView.extend({
        className: "KVStoreFieldView",
        
        defaults: {
        	'field_type' : '',
        	'field_name'  : '',
        	'show_remove' : false
        },
        
        events: {
        	"click .kv-store-field-remove" : "doRemoveField",
        	"change #kv-store-field-name" : "doChangeField"
        },
        
        // Backbone.trigger("field_mapping:selected", this.unique_identifier);
        initialize: function() {
        	this.options = _.extend({}, this.defaults, this.options);
        	
        	this.field_type = this.options.field_type;
        	this.field_name = this.options.field_name;
        	this.show_remove = this.options.show_remove;
        	this.unique_identifier = this.options.unique_identifier;
        },
        template: _.template(Template),
        
        doChangeField: function(){
        	Backbone.trigger("kv_field:changed", this.unique_identifier);
        },
        
        hasFieldName: function(){
        	return this.getFieldName().length > 0;
        },
        
        getFieldName: function(){
        	return $('#kv-store-field-name', this.$el).val();
        },
        
        getFieldType: function(){
        	return $('#kv-store-field-type', this.$el).val();
        },
        
        /**
         * Show an error message
         */
        showErrorMessage: function(message){
        	$('.kv-store-field', this.$el).addClass('error');
        	$('.help-inline', this.$el).text(message);
        },
        
        /**
         * Hide the error message dialog.
         */
        hideErrorMessage: function(){
        	$('.kv-store-field', this.$el).removeClass('error');
        	$('.help-inline', this.$el).text('');
        	
        },
        
        render: function () {
        	
        	this.$el.html(this.template({
        		'show_remove' : this.show_remove,
        		'field_type' : this.field_type,
        		'field_name' : this.field_name
        	}));
        	
        },
        
        doRemoveField: function(){
        	Backbone.trigger("kv_field:remove", this.unique_identifier);
        	this.$el.remove();
        }
        
    });
    
export default KVStoreFieldView;
