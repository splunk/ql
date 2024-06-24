#!/usr/bin/env python3

# File: phantom_forward.py
# Copyright (c) 2016-2024 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

from copy import deepcopy
import os, sys
import csv, gzip
from traceback import format_exc
import json
import re
import urllib
# import requests.packages.urllib3
from sys import platform

try:
    from urllib import unquote
except:
    from urllib.parse import unquote

from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path

script_path = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'phantom', 'bin')
sys.path.insert(0, script_path)

from phantom_config import PhantomConfig, PHANTOM_KEY, VERIFY_KEY, SEVERITIES, get_safe
from phantom_instance import PhantomInstance, NAME_KEY

csv.field_size_limit(10485760)

KV_STORE_PHANTOM_RETRY = "/servicesNS/nobody/phantom/storage/collections/data/phantom_retry"

def load_csv(csv_path):
  if sys.version_info[0] < 3:
    g = gzip.open(csv_path)
  else:
    g = gzip.open(csv_path, 'rt')
  headers = []
  for row in csv.reader(g):
    if not headers:
      headers = row
      continue
    data = dict(zip(headers, row))
    yield data

def fix_multiple_values(result):
  d = dict() # contains keys/values with multiple values
  for i in result:
    try:
        data = result['__mv_' + i]
        r = re.findall(r'(?:\$\$;)?\$(.*?)(?:\$;|\n    \$;|\$$)', data)
        if len(r) > 0:
            d['__mv_' + i] = d[i] = [item.replace('$$', '$') for item in r if item]
    except:
        pass
  return d

def add_cim_to_config(search_config, config):
    cim = config.get_cim_mapping()
    values = search_config.values()
    for k in cim:
        v = get_safe(cim, k, k)
        if v not in search_config and k not in values:
            search_config[v] = k

def forward_csv(config, search_name, csv_path):
    config.logger.info("Search name: {}".format(unquote(search_name)))
    search = None
    for fwd in config.get_forwarding_configs():
        if fwd[NAME_KEY] == search_name:
            search = fwd
            break
    if not search:
        config.logger.error('Error loading config for search {!r}'.format(search_name))
        return

    target = config.get_server_config(fwd['_target'])
    if not target:
        raise Exception('Cannot find search target ({}) in server configurations'.format(search['_target']))
    if not target.get('arrelay'):
      target['arrelay'] = False
    config.logger.info("Target server: '{}'".format(target.get('custom_name')))
    pi = PhantomInstance(target, config.logger, verify=config[VERIFY_KEY], fips_enabled=config.fips_is_enabled)

    # Test connection to SOAR server
    valid_ph_connection = True
    valid_severity = True
    try:
        contains, cef_metadata = pi.verify_server()
    except:
        config.logger.error("Could not verify connection to SOAR. Will be posting to KV Store to retry later")
        valid_ph_connection = False

    container_to_send = []
    artifacts_to_send = []
    container_id = None
    search_results = load_csv(csv_path)
    # config.logger.info("search results: {}".format(search_results))
    for data in search_results:
        # config.logger.info(str({'search_results': data}))
        if search.get('_savedsearch'):
            add_cim_to_config(search, config)
        mul_vals = fix_multiple_values(data)
        for key, value in mul_vals.items():
          data[key] = value
        cef = pi.find_patterns(data, search)

        severity = cef['_severity']
        config_severities = config[SEVERITIES]
        if valid_ph_connection is True and len(config_severities.get(target['ph_auth_config_id'], [])) > 0:
          severity_exists = pi.check_severity(severity)
          if severity_exists is False:
              config.logger.error("Severity '{}' does not exist in SOAR. Sending artifact with 'high' severity and container and artifact tag 'check_sase_severity'.".format(severity))
              valid_severity = False
        cef_copy = deepcopy(cef)
        
        if valid_severity is False:
           cef_copy['_severity'] = 'high'
           cef_copy['tags'] = ['check_sase_severity']
           cef = cef_copy
        artifacts = pi.create_artifacts(cef, data, search)
        config.logger.info(str({'artifacts': artifacts}))
        if not artifacts:
            continue
        key, value = config.splunk.get_return_url(search, artifacts[0].get('data', {}))
        if key and value:
            artifacts[0]['cef'][key] = value
        if valid_ph_connection == True:
          succeeded, container_id, response = pi.get_or_create_container(artifacts[0], cef, search)
          config.logger.info("succeeded: {}, container_id: {}, response: {}".format(succeeded, container_id, response))
          config.logger.info(str({'new_container': container_id}))
        else:
          container_to_send = {"cef": cef, "search_config": search}
        for artifact in artifacts:
            if valid_severity == False:
                 new_artifact = deepcopy(artifact)
                 new_artifact['severity'] = 'high'
                 new_artifact['tags'] = ['check_sase_severity']
                 artifact = new_artifact
            artifact['container_id'] = container_id
            if valid_ph_connection == True:
              artifact_id = pi.post_artifact(artifact)
              config.logger.info(str({'new artifact': artifact_id}))
            else:
              artifacts_to_send.append(artifact)
    if len(container_to_send) > 0:
      try:
        data = {
            'from': "event forwarding",
            'container': container_to_send,
            'artifacts': artifacts_to_send,
            'server_settings': target['ph_auth_config_id']
        }
        success, content = config.splunk.rest_kv(KV_STORE_PHANTOM_RETRY, data, "POST")
        config.logger.info("Posted to KV store for retry later: {}. content: {}".format(success, content))
      except Exception as e:
        config.logger.error("Could not post failed data to KV store. Error {}".format(e))

def remove_carets(data):
  ans = []
  currIdx = 0
  while currIdx < len(data):
    if '\\' == data[currIdx] and '\\' == data[currIdx+1]:
      ans.append("5c".decode("hex"))
      currIdx += 2
    elif '%' == data[currIdx] and '%' == data[currIdx+1]:
      ans.append('%')
      currIdx += 2
    elif '^' == data[currIdx] and '^' == data[currIdx+1] and '!' == data[currIdx+2]:
      ans.append('!')
      currIdx += 3
    elif '^' == data[currIdx] and '^' == data[currIdx+1]:
      ans.append('^')
      currIdx += 2
    elif '^' == data[currIdx]:
      currIdx += 1
    else:
      ans.append(data[currIdx])
      currIdx += 1
  return ''.join(ans)

if __name__ == '__main__':
    try:
        session_key = sys.stdin.readline().strip()
        session_key = session_key[len('sessionKey='):]
        try:
          session_key = urllib.unquote_plus(session_key)
        except:
          session_key = urllib.parse.unquote_plus(session_key)
        # logger = PhantomConfig.get_logger('forwarding')
    except Exception as e:
        logger = PhantomConfig.get_logger('forwarding')
        logger.error('{} called without a session token.'.format(sys.argv[0]))
        sys.exit(0)
    if len(sys.argv) < 9:
        logger = PhantomConfig.get_logger('forwarding')
        # logger.error('{} called without the correct set of parameters.'.format(sys.argv[0]))
        sys.exit(0)
    try:
        config = PhantomConfig('forwarding', session_key)
        csv_path = os.path.join(sys.argv[8])
        search_name = sys.argv[4]
        if search_name.startswith('_phantom_app_'):
            search_name = search_name[13:]
        if platform.startswith('win'):  # If Windows, need to clean up input
            search_name = remove_carets(search_name)
        config.logger.info('csv {!r} search {!r}'.format(csv_path, unquote(search_name)))
        if os.path.exists(csv_path) is True:
          forward_csv(config, search_name, csv_path)
        else:
          config.logger.info("csv_path does not exist. No events found. Exiting...")
    except Exception as e:
        logger = PhantomConfig.get_logger('forwarding')
        logger.error(format_exc())
