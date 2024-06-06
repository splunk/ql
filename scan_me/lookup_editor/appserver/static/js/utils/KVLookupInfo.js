/**
 * This helper will provide an easy way to get the list of users.
 */

import SplunkDBaseModel from "@splunk/swc-lookup/models/SplunkDBase";
import splunkd_utils from "@splunk/swc-lookup/util/splunkd_utils"

	var KVLookup = SplunkDBaseModel.extend({
	    initialize: function() {
	    	SplunkDBaseModel.prototype.initialize.apply(this, arguments);
	    }
	});

    var KVLookupInfo = {

        /**
         * Get information about the given lookup, including:
         *
         *   1) A list of the field types
         *   2) A boolean indicating
         *   3) Whether the lookup is read-only
         *
         * @param namespace
         * @param collection
         */
        getInfo: function(namespace, collection){

            // Get a promise ready
            let promise = jQuery.Deferred();

            // Get the info about the lookup configuration (for KV store lookups)
            var lookup_config = new KVLookup();

            var field_types = {};
            var field_types_enforced = null;
            var read_only = null;
            var replicate = false;

            lookup_config.fetch({
                // e.g. servicesNS/nobody/lookup_editor/storage/collections/config/test
                url: splunkd_utils.fullpath(['/servicesNS', 'nobody', namespace, 'storage/collections/config', collection].join('/')), // For some reason using the actual owner causes this call to fail
                success: function (model, response, options) {
                    console.info("Successfully retrieved the information about the KV store lookup");

                    // Determine the types of the fields
                    for (var possible_field in model.entry.associated.content.attributes) {
                        // Determine if this a field
                        // Check for wordings in the attributes
                        if(possible_field.includes('field.')){
                            field_types[possible_field.substr(6)] = model.entry.associated.content.attributes[possible_field];
                        }
                    }

                    // Determine if types are enforced
                    if (model.entry.associated.content.attributes.hasOwnProperty('enforceTypes')) {
                        if (model.entry.associated.content.attributes.enforceTypes === "true") {
                            field_types_enforced = true;
                        }
                        else {
                            field_types_enforced = false;
                        }
                    }

                    // If this lookup cannot be edited, then set the editor to read-only
                    if (!model.entry.acl.attributes.can_write) {
                        read_only = true;
                    }

                    // If this lookup is being replucated, then set replicate to true
                    if (model.entry.associated.content.attributes.hasOwnProperty('replicate')) {
                        if (model.entry.associated.content.attributes.replicate === "true") {
                            replicate = true;
                        }
                        else {
                            replicate = false;
                        }
                    }

                }.bind(this),
                error: function () {
                    promise.reject();
                    console.warn("Unable to retrieve the information about the KV store lookup");
                }.bind(this),
                complete: function () {
                    promise.resolve(field_types, field_types_enforced, read_only, replicate);
                }.bind(this)
            });

            return promise;
        }
    };

export default KVLookupInfo;
