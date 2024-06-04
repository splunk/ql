/**
 * This provides a simple way to display a modal dialog and respond to the users' input.
 * 
 * 			
        var myModal = new ModalDialog({
				el: $('#my-modal', this.$el),
				title: 'Test this',
				body: 'Are you sure you want to do this?',
				ok_button_title: 'Yes, Do it'
        });

        var myModal.show();
 */
    var _ = require("underscore");
    var SimpleSplunkView = require("splunkjs/mvc/simplesplunkview");

    // Define the custom view class
    var modalDialog = SimpleSplunkView.extend({
        className: "ModalDialog",

        defaults: {
            title: "",
            body: "",
            ok_button_title: null,
            cancel_button_title: "Cancel"
        },
        
        events: {
            "click .btn-primary" : "onPrimary",
            "click .btn-dialog-cancel" : "onCancel"
        },

        /**
         * Initialize the class.
         */
        initialize: function() {
            this.options = _.extend({}, this.defaults, this.options);

            this.is_rendered = false;
            this.promise = null;
        },


        template: _.template('<div tabindex="-1" class="modal fade in hide">' +
            '<div class="modal-header">' +
            '<button type="button" class="close btn-dialog-close" data-dismiss="modal">x</button>' +
            '<h3 class="text-dialog-title"><%- title %></h3>' +
            '</div>' +
            '<div class="modal-body form form-horizontal modal-body-scrolling"><%= body %></div>' +
            '<div class="modal-footer">' +
                '<a href="javascript:void(0)" class="btn btn-dialog-cancel pull-left" data-dismiss="modal" style="display: inline;"><%- cancel_button_title %></a>' +
                '<a href="javascript:void(0)" class="btn btn-primary" data-dismiss="modal" style="display: inline;"><%- ok_button_title %></a>' +
            '</div>' +
        '</div>'),

        /**
         * Show the dialog
         */
        show: function() {
            // Render the modal if necessary
            if(!this.is_rendered){
                this.render();
            }
            var id = this.options.id;

            // Show the modal
            $(function() {
                $(id + " > .modal", this.$el).modal();
            });

            // Make the promise
            this.promise = jQuery.Deferred();
            return this.promise;
        },

        onPrimary: function(){
            this.promise.resolve();
        },

        onCancel: function(){
            this.promise.reject();
        },

        /**
         * Render 
         */
        render: function() {
            this.$el.html(this.template(this.options));
            this.is_rendered = true;
            return this;
        }
    });
export default modalDialog;