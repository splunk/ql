
# encoding = utf-8

# File: modalert_phantom_forward_helper.py
# Copyright (c) 2016-2024 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import os
import csv      ## Result set is in CSV format
import gzip     ## Result set is gzipped
import json     ## Payload comes in JSON format
import logging  ## For specifying log levels
import sys      ## For appending the library path
from datetime import datetime
from traceback import format_exc
import re
import time
import splunk
import splunklib.client as client
import splunklib.results as results

from phantom_config import PhantomConfig, PHANTOM_KEY, get_safe, VERIFY_KEY, SEVERITIES
from phantom_instance import PhantomInstance, NAME_KEY

try:
    from cim_actions import ModularActionTimer
except:
    sys.exit(1)

from splunk.clilib.bundle_paths import make_splunkhome_path
script_path = make_splunkhome_path(["var", "log", "splunk"])
sys.path.insert(0, script_path)

NOTABLE_QUERY = 'search index=notable | where _time>relative_time("{orig_time}", "-3m") AND _time<relative_time("{orig_time}", "+3m") | search orig_bkt="{orig_bkt}" orig_time="{orig_time}" | eval indexer_guid=replace(_bkt,".*~(.+)","\\1"),event_hash=md5(_time._raw),event_id=indexer_guid."@@".index."@@".event_hash,rule_id=event_id | search event_id="*" | fields indexer_guid, event_hash, event_id, index, rule_id | dedup rule_id'

IGNORE = ['_cd', '_serial', '_eventtype_color', '_sourcetype', '_bkt', '_si', '_subsecond', 'eventtype']
KV_STORE_PHANTOM_RETRY = "/servicesNS/nobody/phantom/storage/collections/data/phantom_retry"

def container_from_event(self, result, search_name, group = False):
    container = {}
    container['source_data_identifier'] = str(get_safe(result, 'orig_sid', self.sid))
    if group is False and self.rid:
        container['source_data_identifier'] += '+' + str(get_safe(result, 'orig_rid', self.rid))

    sensitivity = self.settings.get('configuration', {}).get('sensitivity')
    if sensitivity:
        container['sensitivity'] = sensitivity
    container['severity'] = self.severity
    if hasattr(self, "severity_fail"):
        container['tags'] = ['check_sase_severity']
    container['label'] = self.settings.get('configuration', {}).get('label', 'event')

    description = self.settings.get('configuration', {}).get('search_description', '')
    if description == '':
        description = result.get('_phantom_workaround_description', '')
    container['description'] = description

    container_name_setting = self.settings.get('configuration', {}).get('container_name', 'search_name')
    if container_name_setting in ['search_name', ''] and self.action_mode != 'adhoc':
        container['name'] = search_name
    else:
        container['name'] = get_safe(result, 'source', 'Ad hoc search result')

    return container

def format_comment_data(data):
    new_data = data.replace('\n', '\\n')
    value = []
    comments = re.finditer(r'(?:\$\$;)?\$(.*?)(?:\$;|\n    \$;|\$$)', new_data, re.MULTILINE)
    for commentNum, comment in enumerate(comments, start=1):
        for groupNum in range(0, len(comment.groups())):
            groupNum = groupNum + 1
            group = comment.group(groupNum)
            new_group = group.replace('\\n', '\n')
            value.append(new_group)
    return value

def check_for_custom_multiple_values(result):
    d = dict() # contains keys/values with multiple values
    custom_keys = []
    for i in result:
        if i not in IGNORE and not i.startswith('__mv_'): # and not i.startswith('orig_'):
            custom_keys.append(i)
    for i in custom_keys:
        if i == 'comment':
            comment_value = format_comment_data(result.get('__mv_comment', ''))
            if len(comment_value) > 0:
                d[i] = comment_value
        else:
            try:
                data = result['__mv_' + i]
                r = re.findall(r'(?:\$\$;)?\$(.*?)(?:\$;|\n    \$;|\$$)', data)
                if len(r) > 0:
                    d[i] = [item.replace('$$', '$') for item in r if item]
            except:
                pass
    if len(d) > 0:
        return True, d, custom_keys
    return False, d, custom_keys

def artifact_from_event(self, result, container, config, additional_keys):
    notable = {
        "orig_time": None,
        "orig_bkt": None,
        "orig_raw": None
    }

    artifact = {}
    artifact['cef'] = cef = {}
    artifact['data'] = data = { 'action_name': self.action_name }
    artifact['name'] = self.settings.get('search_name', '')
    try:
        artifact['container_id'] = container['id']
    except:
        pass
    artifact['source_data_identifier'] = container['source_data_identifier']
    if hasattr(self, "severity_fail"):
        artifact['tags'] = ['check_sase_severity']
    artifact['severity'] = self.severity
    artifact['label'] = self.settings.get('configuration', {}).get('label', 'event')
    cim_cef_map = additional_keys
    cim_cef_map.update(config.get_cim_mapping())
    for k, v in result.items():
        if k == '_time':
            artifact['start_time'] = artifact['end_time']  = datetime.utcfromtimestamp(float(v)).isoformat() + 'Z'
            data[k] = v
            notable["orig_time"] = v
        elif k == '_raw':
            data[k] = v
            notable["orig_raw"] = v
        elif k == 'search_name' and artifact['name'] == '':
            artifact['name'] = v
        elif k == '_phantom_workaround_description':
            continue
        elif not v:
            continue
        else:
            if k == '_bkt':
                notable["orig_bkt"] = v
            cef_k = get_safe(cim_cef_map, k, None)
            data[k] = v
            if cef_k:
                cef[cef_k] = v
            elif k in cim_cef_map:
                cef[k] = v
            

    # Only works if not using AR Relay since you cannot search events on the SH from the HF
    if all(value is not None for value in notable.values()) and self.is_arr is False:
        notable_data = search_splunk(self, notable, 'notable_event_id')
        event_id = notable_data.get('event_id')
        if event_id:
            cef.update({ 'event_id': event_id })
            data.update({ 'event_id': event_id })
            artifact.update({ 'event_id': event_id })
        # cef.update(notable_data)
        # data.update(notable_data)
        # artifact.update(notable_data)

    return artifact

def get_severity(self):
    original_severity = self.settings.get('configuration', {}).get('severity', 'medium')
    try:
        r = re.compile('(.*):\s*(.*)')
        server = r.search(original_severity).group(1)
        severity = r.search(original_severity).group(2)
        return severity
    except:
        return original_severity

def get_artifact_send_method(self):
    path = '/servicesNS/nobody/phantom/configs/conf-phantom/artifact_ar?output_mode=json'
    try:
        args = {
            'method': 'GET',
            'sessionKey': self.session
        }
        response, content = splunk.rest.simpleRequest(path, **args)
        content = json.loads(content)
        value = content.get('entry', [])[0].get('content', {}).get('value')
        return value
    except Exception as e:
        self.logger.info(f"Could not retrieve method. {e}")

def search_splunk(self, info, query_type):
    time.sleep(8)
    service = client.connect(token=self.session)
    kwargs = {
        "output_mode": "json",
        "ttl": 45
    }

    query = None
    # Query for the notable event_id if a notable event is created when AR is invoked
    if query_type == 'notable_event_id':
        query = NOTABLE_QUERY.format(orig_time=info.get('orig_time'), orig_bkt=info.get('orig_bkt'))

    job = service.jobs.create(query, **kwargs)

    while True:
        while not job.is_ready():
            pass
        stats = {"isDone": job["isDone"],
             "doneProgress": float(job["doneProgress"])*100,
              "scanCount": int(job["scanCount"]),
              "eventCount": int(job["eventCount"]),
              "resultCount": int(job["resultCount"])}

        status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
                "%(eventCount)d matched   %(resultCount)d results") % stats

        sys.stdout.write(status)
        sys.stdout.flush()
        if stats["isDone"] == "1":
            sys.stdout.write("\n\nDone!\n\n")
            break
        time.sleep(2)

    data = {}
    reader = results.JSONResultsReader(job.results(output_mode='json'))
    for result in reader:
        if isinstance(result, dict):
            data = result
        elif isinstance(result, results.Message):
            # Diagnostic messages may be returned in the results
            self.log_debug(f"Diagnostic reader result Message: {result}")

    job.cancel()

    return data


def _add_event(self, message):
    if type(message) in (dict, list):
        message = json.dumps(message)
    self.addevent(message, sourcetype='phantom_automation')

def _write_events(self):
    if self.settings.get('configuration', {}).get('server_playbook_name'):
        source = 'phantom_runphantomplaybook_modalert.log'
    else:
        source = 'phantom_sendtophantom_modalert.log'
    path = os.path.join(script_path, source)
    self.writeevents(index="cim_modactions", host="localhost", source=path)

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the alert action parameters and prints them to the log
    dropdown_list = helper.get_param("dropdown_list")
    helper.log_info("dropdown_list={}".format(dropdown_list))

    dropdown_list_1540256443831 = helper.get_param("dropdown_list_1540256443831")
    helper.log_info("dropdown_list_1540256443831={}".format(dropdown_list_1540256443831))

    dropdown_list_1540256445876 = helper.get_param("dropdown_list_1540256445876")
    helper.log_info("dropdown_list_1540256445876={}".format(dropdown_list_1540256445876))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    logger = 'forward_modalert'
    config = None
    helper.session = None

    server = helper.settings.get('configuration', {}).get('phantom_server')
    playbook = helper.settings.get('configuration', {}).get('playbook_name')
    server_playbook_name = helper.settings.get('configuration', {}).get('server_playbook_name')
    if server_playbook_name:
        r = re.compile('(.*):\s*(.*)')
        server = r.search(server_playbook_name).group(1)
        playbook = r.search(server_playbook_name).group(2)
    else:
        server_playbook_name = f"{server}: {playbook}"

    # Used for AR relay
    helper.is_arr = False
    if server.endswith(' (ARR)'):
        helper.log_info("Running AR Relay")
        if helper.settings.get('configuration', {}).get('_cam_workers') and helper.settings.get('configuration', {}).get('_cam_workers', '["local"]') in ['', '["local"]', '[\"local\"]']:
            helper.log_error("Worker Set provided was 'local', but an ARR server was provided")
            _write_events(helper)
            return 3
        user = helper.settings.get('configuration', {}).get('relay_details', {}).get('username')
        password = helper.settings.get('configuration', {}).get('relay_details', {}).get('password')
        if not user or not password:
            helper.log_error("Incomplete relay details received")
            _write_events(helper)
            return 3
        splunkService = client.connect(username=user, password=password)
        helper.session = splunkService.token[7:]
        config = PhantomConfig(logger, helper.session)

        # Remove (ARR) helper
        helper.is_arr = True
        server = server[:-6]
    else:
        helper.log_info("Running locally")
        helper.session = helper.settings.get('session_key')
        config = PhantomConfig(logger, helper.session)

    artifact_distribution = get_artifact_send_method(helper)
    artifact_distribution_msg = 'a single event' if artifact_distribution == '\"single\"' or artifact_distribution == '\'single\'' else 'multiple events'

    grouping = helper.settings.get('configuration', {}).get('grouping', '0')
    group = True if grouping == '1' else False
    multiple_container_msg = ' and grouped into a single container' if group is True else ''

    helper.log_info(f"Running action '{helper.action_name}' to forward {artifact_distribution_msg} to '{server}'{multiple_container_msg}")

    server_settings = None
    for i in config[PHANTOM_KEY]:
        if helper.is_arr is False and server == 'Default' and str(config[PHANTOM_KEY][i]['default']).lower() in ["true", "default"]:
            server_settings = config[PHANTOM_KEY][i]
            break
        elif server == config[PHANTOM_KEY][i]['custom_name']:
            server_settings = config[PHANTOM_KEY][i]
            break
    if not server_settings:
        helper.log_error(f'Alert expected target "{server}", but target and password do not exist in SOAR Server Configuration.')
        helper.message("", status="failure")
        _write_events(helper)
        return 3

    try:
        server_settings['proxy'] = server_settings['proxy']['https']
    except:
        server_settings['proxy'] = ''

    if not server_settings.get('arrelay'):
        server_settings['arrelay'] = False    
    pi = PhantomInstance(server_settings, config.logger, verify=config[VERIFY_KEY], fips_enabled=config.fips_is_enabled)

    # Test connection to Phantom server
    valid_ph_connection = True
    try:
        contains, cef_metadata = pi.verify_server()
    except:
        helper.log_error("Could not verify connection to SOAR. Will be posting to KV Store to retry later")
        valid_ph_connection = False

    helper.severity = get_severity(helper)
    severity_exists = True
    target_custom_severities = config[SEVERITIES].get(server_settings.get('ph_auth_config_id'), [])
    if valid_ph_connection is True:
        if len(target_custom_severities) > 0:
            severity_exists = pi.check_severity(helper.severity)
        else:
            severity_exists = helper.severity.lower() in ['high', 'medium', 'low']
        if severity_exists is False:
            helper.log_error(f"Severity '{helper.severity}' does not exist in SOAR. Sending artifact with 'high' severity and container and artifact tag 'check_sase_severity'.")
            helper.severity = 'high'
            helper.severity_fail = True

    results = []
    with ModularActionTimer(helper, 'main', helper.start_timer):
        with gzip.open(helper.results_file, 'rt') as fh:
            for num, result in enumerate(csv.DictReader(fh)):
                result.setdefault('rid', num)
                result.setdefault('sid', helper.settings.get('sid'))
                result.setdefault('tag', 'modaction')
                helper.update(result)
                # helper.invoke()
                notable_data = {
                    'action_name': str(helper.settings.get('configuration', {}).get('action_name')),
                    'sid': str(helper.settings.get('sid'))
                }
                container = container_from_event(helper, result, helper.settings.get('search_name'), group)
                container_to_send = []
                artifacts_to_send = []
                playbook_to_send = None
                try:
                    if valid_ph_connection is True:
                        response = pi.post('/rest/container', container)
                        response = response.json()
                        if 'Severity matching query does not exist.' in response.get('message', ''):
                            helper.log_error("Severity label does not exist in SOAR. Sending event with artifact tag 'check_sase_severity'.")
                            valid_ph_connection = False
                            container['severity'] = 'high'
                            container_to_send = container
                            helper.severity_fail = True
                        else:
                            container_id = response.get('id')
                            created = True
                            if not container_id:
                                container_id = response.get('existing_container_id')
                                created = False
                            if not container_id:
                                helper.log_error(f"Unable to create container: {response.get('message')}")
                                helper.message("", status="failure")
                                _write_events(helper)
                                return 1
                            if created:
                                _add_event(helper, response)
                            container['id'] = container_id
                            resp = notable_data.copy()
                            resp.update({ 'container_id' : container['id'], 'container_url': '{}/mission/{}'.format(pi.server, container['id']), 'success': 'true' })
                            _add_event(helper, resp)
                    else:
                        container_to_send = container
                    loop, mul_vals, custom_keys = check_for_custom_multiple_values(result)
                    additional_keys = {"{}".format(x): "{}".format(x) for x in custom_keys}
                    if loop:
                        mul_keys = mul_vals.keys()
                        new_res = dict()
                        if artifact_distribution == '\"single\"' or artifact_distribution == '\'single\'':
                            new_res = mul_vals
                            for z in result:
                                if z not in mul_keys:
                                    new_res[z] = result[z]
                            
                            artifact = artifact_from_event(helper, new_res, container, config, additional_keys)
                            artifact['cef']['_originating_search'] = helper.settings.get('results_link')
                            if valid_ph_connection is True:
                                created, artifact_id, response, c = pi.post_artifact(artifact)
                                results.append((container, artifact))
                                resp = notable_data.copy()
                                resp.update(response.json())
                                _add_event(helper, resp)
                            else:
                                artifacts_to_send.append(artifact)
                        else:
                            # Get largest list
                            largest = { 'key': '', 'size': 0 }
                            for key, value in mul_vals.items():
                                if len(value) > largest['size']:
                                    largest['key'] = key
                                    largest['size'] = len(value)
                            # Make largest list the pivot list
                            pivot_list = mul_vals[largest['key']]
                            # del mul_vals[largest['key']]
                            for i in range(len(pivot_list)):
                                if i > 999:
                                    helper.log_info("Max 1,000 artifacts sent to SOAR. Additional artifacts not sent.")
                                    break
                                new_res = { largest['key']: pivot_list[i] }
                                for z in result:
                                    if z not in mul_keys:
                                        new_res[z] = result[z]
                                for x in mul_vals:
                                    try:
                                        new_res[x] = mul_vals[x][i]
                                    except:
                                        new_res[x] = mul_vals[x][0]

                                artifact = artifact_from_event(helper, new_res, container, config, additional_keys)
                                artifact['cef']['_originating_search'] = helper.settings.get('results_link')
                                if valid_ph_connection is True:
                                    created, artifact_id, response, c = pi.post_artifact(artifact)
                                    results.append((container, artifact))
                                    resp = notable_data.copy()
                                    resp.update(response.json())
                                    _add_event(helper, resp)
                                else:
                                    artifacts_to_send.append(artifact)
                    else:
                        artifact = artifact_from_event(helper, result, container, config, additional_keys)
                        artifact['cef']['_originating_search'] = helper.settings.get('results_link')
                        if valid_ph_connection is True:
                            created, artifact_id, response, c = pi.post_artifact(artifact)
                            results.append((container, artifact))
                            resp = notable_data.copy()
                            resp.update(response.json())
                            _add_event(helper, resp)
                        else:
                            artifacts_to_send.append(artifact)
                    if playbook:
                        payload = {
                            'run': True,
                            'playbook_id': playbook,
                        }
                        try:
                            payload['container_id'] = container['id']
                        except:
                            pass
                        if valid_ph_connection is True:
                            response = pi.post('/rest/playbook_run', payload)
                            if response.status_code != 200:
                                message = 'Failed to run playbook: message:{}'.format(response.text)
                                _add_event(helper, message)
                                _write_events(helper)
                                return 1
                            else:
                                message = 'Playbook run. ID is {}'.format(get_safe(response.json(), 'playbook_run_id', 'MISSING ID'))
                                _add_event(helper, message)
                                _add_event(helper, [response.json()])
                        else:
                            playbook_to_send = payload
                except:
                    helper.log_error(f"Error while creating artifacts: {format_exc()}")
                    helper.message("", status="failure")
                    return 5

                if len(container_to_send) > 0:
                    try:
                        data = {
                            'from': 'notable',
                            'container': container_to_send,
                            'artifacts': artifacts_to_send,
                            'playbook': playbook_to_send,
                            'server_settings': server_settings['ph_auth_config_id']
                        }
                        success, content = config.splunk.rest_kv(KV_STORE_PHANTOM_RETRY, data, "POST")
                        helper.log_info(f"Posted to KV store for retry later: {success}. content: {content}")
                    except Exception as e:
                        helper.log_error(f"Could not post failed data to KV store. Error {format(e)}")
                        helper.message("", status="failure")
            if result.get('_phantom_workaround_description'):
                result.pop('_phantom_workaround_description')
            ## rate limiting
            time.sleep(1.6)
    _write_events(helper)
    return 0
