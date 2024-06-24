"""
    Check to see if notable was sent over to Phantom. If notable did not make it to Phantom, try to send it over with a new POST via REST
    1. If there is a blocked connection between Splunk and Phantom, the event will still eventually send once connection is restored
    2. If Phantom is down and Splunk is trying to send a notable, the notable will never make it to Phantom
    3. If the Phantom config is wrong (ie invalid ph-auth-token), the notable will never make it to Phantom
    Scenarios 2. and 3. need to be addressed by this mod input script

    Error(s) seen in modalert_phantom_forward_helper.py for 2.:
        Line 331: Error while creating container: Traceback (most recent call last)
    Error(s) seen in modalert_phantom_forward_helper.py for 3.:
        Line 331: Unable to create container: authentication failure
"""

# File: phantom_retry.py
# Copyright (c) 2016-2024 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

from copy import deepcopy
import sys
import json
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path
from splunk.clilib.bundle_paths import make_splunkhome_path
from phantom_config import PhantomConfig, PHANTOM_KEY, VERIFY_KEY, SEVERITIES, get_safe
from phantom_instance import PhantomInstance, NAME_KEY

from phantom_imports import (
    KV_STORE_PHANTOM_ENDPOINT,
    KV_STORE_PHANTOM_RETRY
)

script_path = make_splunkhome_path(["etc", "apps", "phantom", "bin"])
sys.path.insert(0, script_path)

COMPONENT_RETRY = 'retry'
INVALID_LABEL_ERROR = "is not a known label."

# Empty introspection routine
def do_scheme():
    pass

def get_kv_store_count(config):
    count = 0
    args = {
        'search': '| inputlookup phantom_retry_lookup | stats count'
    }
    success, content = config.splunk.search(args)
    if success is True:
        if len(content) == 0:
            return int(-1)
        json_content = json.loads(content)
        count = json_content.get('result', {}).get('count', 0)

    return int(count)

def query_kv_store(config, logger, collection):
    uri = "{endpoint}/{collection}".format(endpoint=KV_STORE_PHANTOM_ENDPOINT, collection=collection)
    success, content = config.splunk.rest_kv(uri, {'limit': 250}, "GET")
    if success is True:
        content = json.loads(content.decode('utf-8'))
        if len(content) > 0:
            for item in content:
                can_delete_from_kv = True
                try:
                    container_id = None
                    server = config[PHANTOM_KEY]
                    config_id = item['server_settings']
                    server_settings = server[config_id]
                    pi = PhantomInstance(server_settings, config.logger, config[VERIFY_KEY], fips_enabled=config.fips_is_enabled)

                    # Exit early if no valid connection to SOAR sever
                    valid_ph_connection = True
                    try:
                        contains, cef_metadata = pi.verify_server()
                    except:
                        valid_ph_connection = False
                        can_delete_from_kv = False
                        config.logger.error(f"Could not verify connection to SOAR server '{server_settings['custom_name']}'. Retry post to SOAR later.")

                    if valid_ph_connection == True:
                        severity_exists = True
                        severity = 'high'
                        target_custom_severities = config[SEVERITIES].get(config_id, [])
                        original_severity = ''
                        if item['from'] == 'notable':
                            severity = item['container']['severity']
                            original_severity = item['container']['severity']
                        else:
                            severity = item['container']['search_config']['_severity']
                            original_severity = item['container']['search_config']['_severity']

                        if len(target_custom_severities) > 0:
                            severity_exists = pi.check_severity(severity)
                        else:
                            severity_exists = severity.lower() in ['high', 'medium', 'low']

                        if severity_exists is False:
                            config.logger.error(f"Severity '{original_severity}' does not exist in SOAR. Sending container with 'high' severity and container tag 'check_sase_severity'.")
                            severity = 'high'
                            if item['from'] == 'notable':
                                item['container']['severity'] = severity
                                item['container']['tags'] = ['check_sase_severity']
                            else:
                                item['container']['search_config']['_severity'] = severity
                                item['container']['search_config']['tags'] = ['check_sase_severity']
                        else:
                            if item['from'] == 'notable':
                                severity = item['container']['severity']
                            else:
                                severity = item['container']['search_config']['_severity']

                        if item['from'] == 'notable':
                            config.logger.info("Found a failed alert action to retry")
                            sdi = item['container']['source_data_identifier']
                            name = item['container']['name']
                            config.logger.info("Trying rule_id '{name}' source_data_identifier '{sdi}'".format(name=name, sdi=sdi))

                            # Try creating container in SOAR
                            response = pi.post('/rest/container', item['container'])
                            resp_json = response.json()
                            container_id = response.json().get('id')
                            if not container_id:
                                container_id = response.json().get('existing_container_id')
                            if not container_id:
                                message = response.json().get('message')
                                if INVALID_LABEL_ERROR in message:
                                    config.logger.info("Attempting to delete failed item containing invalid label from KV Store")
                                    uri_item = "{uri}/{key}".format(uri=uri, key=item['_key'])
                                    success, content = config.splunk.rest_kv(uri_item, {}, 'DELETE')
                                    if success is True:
                                        config.logger.info("Failed item contained invalid label. Item deleted from KV Store")
                                else:
                                    config.logger.error('Unable to create container: ' + response.json().get('message'))
                                    can_delete_from_kv = False
                                continue
                            else:
                                server = server_settings['server']
                                msg = { 'container_id': container_id, 'container_url': '{server}/mission/{container_id}'.format(server=server, container_id=container_id), 'success': 'true' }
                                config.logger.info(msg)
                            # Try creating artifact(s) for the container
                            for art in item['artifacts']:
                                art_item = art
                                art_item.update({ 'container_id': container_id })
                                if severity_exists is False:
                                    config.logger.info(f"Severity '{art_item['severity']}' does not exist in SOAR. Sending artifact with 'high' severity and artifact tag 'check_sase_severity.")
                                    art_item.update({ 'severity': severity, 'tags': ['check_sase_severity'] })
                                created, artifact_id, response, c = pi.post_artifact(art_item)
                                resp_json = response.json()
                                config.logger.info(resp_json)
                                if created is False and resp_json.get('existing_artifact_id') is None:
                                    can_delete_from_kv = False
                            if item.get('playbook') is not None:
                                playbook_item = item['playbook']
                                playbook_item.update({ 'container_id': container_id })
                                response = pi.post('/rest/playbook_run', item['playbook'])
                                if response.status_code != 200:
                                    message = 'Failed to run playbook: message:{}'.format(response.text)
                                    config.logger.info(message)
                                else:
                                    message = 'Playbook run. ID is {}'.format(get_safe(response.json(), 'playbook_run_id', 'MISSING ID'))
                                    config.logger.info(message)
                        elif item['from'] == 'event forwarding':
                            config.logger.info("Found a failed event forwarding to retry")
                            for art in item['artifacts']:
                                item_artifact = art
                                cef = item['container']['cef']
                                sensitivity = item['container']['cef']['_sensitivity']
                                severity = item['container']['cef']['_severity']
                                item_cef = deepcopy(cef)
                                item_search_config = deepcopy(item['container']['search_config'])
                                key, value = config.splunk.get_return_url(item_search_config, item_artifact.get('data', {}))
                                if key and value:
                                    item_artifact['cef'][key] = value
                                succeeded, container_id, response = pi.get_or_create_container(item_artifact, item_cef, item_search_config)
                                config.logger.info("succeeded: {}, container_id: {}, response: {}".format(succeeded, container_id, response))
                                if 'Severity matching query does not exist.' in str(response):
                                    config.logger.error(f"Severity '{severity}' does not exist in SOAR. Sending container with 'high' severity and container tag 'check_sase_severity'.")
                                    item_cef['_sensitivity'] = sensitivity
                                    item_cef['_severity'] = 'high'
                                    item_cef['tags'] = ['check_sase_severity']
                                    succeeded, container_id, response = pi.get_or_create_container(item_artifact, item_cef, item_search_config)
                                config.logger.info(str({'new_container': container_id}))

                                item_artifact.update({ 'container_id': container_id })
                                created, artifact_id, response, c = pi.post_artifact(item_artifact)
                                resp_json = response.json()
                                if 'Severity matching query does not exist.' in resp_json.get('message', ''):
                                    config.logger.info(f"Severity '{item_artifact['severity']}' does not exist in SOAR. Sending artifact with 'high' severity and artifact tag 'check_sase_severity.")
                                    item_artifact.update({
                                        'severity': 'high',
                                        'tags': ['check_sase_severity']
                                    })
                                    created, artifact_id, response, c = pi.post_artifact(item_artifact)
                                    resp_json = response.json()
                                    config.logger.info(resp_json)
                                else:
                                    config.logger.info(resp_json)
                                if created is False and resp_json.get('existing_artifact_id') is None:
                                    can_delete_from_kv = False
                        
                    if can_delete_from_kv is True:
                        uri_item = "{uri}/{key}".format(uri=uri, key=item['_key'])
                        success, content = config.splunk.rest_kv(uri_item, {}, 'DELETE')
                        if success is True:
                            config.logger.info("Failed item is now posted to SOAR. Item deleted from KV Store")
                except Exception as e:
                    message = str(e)
                    if INVALID_LABEL_ERROR in message:
                        config.logger.info("Attempting to delete failed item containing invalid label from KV Store")
                        uri_item = "{uri}/{key}".format(uri=uri, key=item['_key'])
                        success, content = config.splunk.rest_kv(uri_item, {}, 'DELETE')
                        if success is True:
                            config.logger.info("Failed item contained invalid label. Item deleted from KV Store")
                    else:
                        pass
    else:
        config.logger.error("Error retrieving items from KV Store {collection}".format(collection=collection))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            if len(sys.argv)>3:
                validate_config(sys.argv[2],sys.argv[3])
            else:
                print('supply username and password')
        elif sys.argv[1] == "--test":
            print('No tests for the scheme present')
        else:
            print('You giveth weird arguments')
    else:
        session_key = sys.stdin.read()
        if not session_key:
            print("No session key received. Exiting")
            sys.exit(1)

        config = PhantomConfig(COMPONENT_RETRY, session_key)
        try:
            config.logger.info("Mod Input Retry")
            num_items = get_kv_store_count(config)
            if num_items > 0:
                config.logger.info("Num items in KV Store: {}".format(num_items))
                query_kv_store(config, config.logger, KV_STORE_PHANTOM_RETRY)
            elif num_items == -1:
                config.logger.info("Mod input initializing...")
            else:
                config.logger.info("No items found in KV Store {collection}".format(collection=KV_STORE_PHANTOM_RETRY))
        except Exception as e:
            config.logger.error("Error: {}".format(e))
    sys.exit(0)
