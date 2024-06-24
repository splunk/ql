# File: phantom_instance.py
# Copyright (c) 2016-2024 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import os, sys
from traceback import format_exc
import json
from unicodedata import name

try:
    from urllib import quote, unquote, quote_plus
except:
    from urllib.parse import quote, unquote, quote_plus

from copy import deepcopy
import hashlib

if sys.version_info >= (3, 0):
   from io import StringIO
   import configparser
else:
   from StringIO import StringIO
   import ConfigParser as configparser


script_path = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'phantom', 'bin')
sys.path.insert(0, script_path)
import phantom_requests as requests

try:
    from .phantom_config import PhantomConfig, get_safe, TOKEN_KEY
except:
    from phantom_config import PhantomConfig, get_safe, TOKEN_KEY

PKS = '__pks[]'
SEVERITY_KEY = '_severity'
SENSITIVITY_KEY = '_sensitivity'
NAME_OVERRIDE_KEY = '_container_name'
NAME_KEY = '_name'
TAGS_KEY = 'tags'

VALID_SEV = ('high', 'low', 'medium')
VALID_SENS = ('red', 'green', 'amber', 'white')
DEFAULT_SEV = 'medium'
DEFAULT_SENS = 'amber'

CERT_FILE_LOCATION_DEFAULT = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'phantom', 'default', 'cert_bundle.pem')
CERT_FILE_LOCATION_LOCAL = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'phantom', 'local', 'cert_bundle.pem')

DEFAULT_CONTAINS = [
        'ip',
        'user name',
        'port',
        'mac address',
        'host name',
        'domain',
        'url',
        'file path',
        'file name',
        'hash',
        'process name',
        'email'
]

DEFAULT_CEF_METADATA = {
    "act": {'contains': []},
    "app": {'contains': []},
    "applicationProtocol": {'contains': []},
    "baseEventCount": {'contains': []},
    "bytesIn": {'contains': []},
    "bytesOut": {'contains': []},
    "cat": {'contains': []},
    "cn1": {'contains': []},
    "cn1Label": {'contains': []},
    "cn2": {'contains': []},
    "cn2Label": {'contains': []},
    "cn3": {'contains': []},
    "cn3Label": {'contains': []},
    "cnt": {'contains': []},
    "cs1": {'contains': []},
    "cs1Label": {'contains': []},
    "cs2": {'contains': []},
    "cs2Label": {'contains': []},
    "cs3": {'contains': []},
    "cs3Label": {'contains': []},
    "cs4": {'contains': []},
    "cs4Label": {'contains': []},
    "cs5": {'contains': []},
    "cs5Label": {'contains': []},
    "cs6": {'contains': []},
    "cs6Label": {'contains': []},
    "destinationAddress": {'contains': ['ip', ]},
    "destinationDnsDomain": {'contains': ['domain']},
    "destinationHostName": {'contains': ['host name']},
    "destinationMacAddress": {'contains': ['mac address']},
    "destinationNtDomain": {'contains': []},
    "destinationPort": {'contains': ['port']},
    "destinationProcessName": {'contains': ['process name']},
    "destinationServiceName": {'contains': ['process name']},
    "destinationTranslatedAddress": {'contains': ['ip']},
    "destinationTranslatedPort": {'contains': ['port']},
    "destinationUserId": {'contains': []},
    "destinationUserName": {'contains': ['user name']},
    "destinationUserPrivileges": {'contains': []},
    "deviceAction": {'contains': []},
    "deviceAddress": {'contains': ['ip']},
    "deviceCustomDate1": {'contains': []},
    "deviceCustomDate1Label": {'contains': []},
    "deviceCustomDate2": {'contains': []},
    "deviceCustomDate2Label": {'contains': []},
    "deviceCustomNumber1": {'contains': []},
    "deviceCustomNumber1Label": {'contains': []},
    "deviceCustomNumber2": {'contains': []},
    "deviceCustomNumber2Label": {'contains': []},
    "deviceCustomNumber3": {'contains': []},
    "deviceCustomNumber3Label": {'contains': []},
    "deviceCustomString1": {'contains': []},
    "deviceCustomString1Label": {'contains': []},
    "deviceCustomString2": {'contains': []},
    "deviceCustomString2Label": {'contains': []},
    "deviceCustomString3": {'contains': []},
    "deviceCustomString3Label": {'contains': []},
    "deviceCustomString4": {'contains': []},
    "deviceCustomString4Label": {'contains': []},
    "deviceCustomString5": {'contains': []},
    "deviceCustomString5Label": {'contains': []},
    "deviceCustomString6": {'contains': []},
    "deviceCustomString6Label": {'contains': []},
    "deviceDirection": {'contains': []},
    "deviceDnsDomain": {'contains': ['domain']},
    "deviceEventCategory": {'contains': []},
    "deviceExternalId": {'contains': []},
    "deviceFacility": {'contains': []},
    "deviceHostname": {'contains': ['host name']},
    "deviceInboundInterface": {'contains': []},
    "deviceMacAddress": {'contains': ['mac address']},
    "deviceOutboundInterface": {'contains': []},
    "deviceProcessName": {'contains': ['process name']},
    "deviceTranslatedAddress": {'contains': ['ip']},
    "dhost": {'contains': ['host name']},
    "dmac": {'contains': ['mac address']},
    "dntdom": {'contains': ['domain']},
    "dpriv": {'contains': []},
    "dproc": {'contains': ['process name']},
    "dpt": {'contains': ['port']},
    "dst": {'contains': ['ip']},
    "duid": {'contains': []},
    "duser": {'contains': ['user name']},
    "dvc": {'contains': ['ip']},
    "dvchost": {'contains': ['host name']},
    "end": {'contains': []},
    "endTime": {'contains': []},
    "externalId": {'contains': []},
    "eventOutcome": {'contains': []},
    "fileCreateTime": {'contains': []},
    "fileHash": {'contains': ['hash']},
    "fileId": {'contains': []},
    "fileModificationTime": {'contains': []},
    "fileName": {'contains': ['file name']},
    "filePath": {'contains': ['file path']},
    "filePermission": {'contains': []},
    "fileSize": {'contains': []},
    "fileType": {'contains': []},
    "fname": {'contains': ['file name']},
    "fsize": {'contains': []},
    "in": {'contains': []},
    "message": {'contains': []},
    "msg": {'contains': []},
    "oldfileCreateTime": {'contains': []},
    "oldfileHash": {'contains': ['hash']},
    "oldfileId": {'contains': []},
    "oldfileModificationTime": {'contains': []},
    "oldfileName": {'contains': ['file name']},
    "oldfilePath": {'contains': ['file path']},
    "oldfilePermission": {'contains': []},
    "oldfileType": {'contains': []},
    "oldfsize": {'contains': []},
    "out": {'contains': []},
    "outcome": {'contains': []},
    "proto": {'contains': []},
    "receiptTime": {'contains': []},
    "request": {'contains': []},
    "requestClientApplication": {'contains': []},
    "requestCookies": {'contains': []},
    "requestMethod": {'contains': []},
    "requestURL": {'contains': ['url']},
    "rt": {'contains': []},
    "shost": {'contains': ['host name']},
    "smac": {'contains': ['mac address']},
    "sntdom": {'contains': ['domain']},
    "sourceAddress": {'contains': ['ip']},
    "sourceDnsDomain": {'contains': ['domain']},
    "sourceHostName": {'contains': ['host name']},
    "sourceMacAddress": {'contains': ['mac address']},
    "sourceNtDomain": {'contains': []},
    "sourcePort": {'contains': ['port']},
    "sourceServiceName": {'contains': []},
    "sourceTranslatedAddress": {'contains': ['ip']},
    "sourceTranslatedPort": {'contains': ['port']},
    "sourceUserId": {'contains': []},
    "sourceUserName": {'contains': ['user name']},
    "sourceUserPrivileges": {'contains': []},
    "spriv": {'contains': []},
    "spt": {'contains': ['port']},
    "src": {'contains': ['ip']},
    "start": {'contains': []},
    "startTime": {'contains': []},
    "suid": {'contains': []},
    "suser": {'contains': ['user name']},
    "transportProtocol": {'contains': []},
}

class PhantomInstance(object):
    def __init__(self, config_entry, logger, verify=False, fips_enabled=False):
        self.logger = logger
        self._config = config_entry
        self.ph_auth_config_id = config_entry['ph_auth_config_id']
        self.custom_name = config_entry['custom_name']
        self.default = config_entry['default']
        self.server = config_entry['server']
        self.token = config_entry[TOKEN_KEY]
        self.arrelay = config_entry['arrelay']
        self.auth_headers = {
            'ph-auth-token': self.token,
            'Content-Type': 'application/json'
        }
        self.user = config_entry.get('user', '')
        self.verify = bool(verify)
        if self.verify and os.path.isfile(CERT_FILE_LOCATION_LOCAL):
            self.verify = CERT_FILE_LOCATION_LOCAL
        elif self.verify and os.path.isfile(CERT_FILE_LOCATION_DEFAULT):
            self.verify = CERT_FILE_LOCATION_DEFAULT
        PhantomInstance.fips_enabled = fips_enabled
        self._cef_metadata = {}
        self._all_contains = {}
        self._set_proxy()

    @classmethod
    def fips_enabled(cls):
        return PhantomInstance.fips_enabled

    def cef_metadata(self):
        if not self._cef_metadata:
            self._load_cef_metadata()
        return self._cef_metadata

    def contains(self):
        if not self._all_contains:
            self._load_cef_metadata()
        return self._all_contains

    def _load_cef_metadata(self):
        base_uri = "{}/rest/cef_metadata".format(self.server)
        try:
            response = requests.get(base_uri, headers=self.auth_headers, verify=self.verify, proxies=self.proxy)
            response_json = response.json()
            if response.status_code != 200:
                raise Exception(response_json.get('message', 'Failed'))

            self._all_contains = set(DEFAULT_CONTAINS)
            self._cef_metadata = response_json.get('cef', {})
            for key, value in self._cef_metadata.items():
                if not self._cef_metadata.get(key) or 'contains' not in self._cef_metadata[key]:
                    self._cef_metadata[key] = { 'contains': [] }
                contains = self._cef_metadata[key]['contains']
                self._all_contains.update(value.get('contains', []))

            self._all_contains.update(response_json.get('all_contains', []))
            if '*' in self._all_contains:
                self._all_contains.remove('*')
            self._all_contains = list(self._all_contains)
            # self.logger.debug(self._all_contains)
        except Exception:
            self.logger.error(format_exc())
            raise

    def _set_proxy(self):
        self.proxy = None
        original_proxy = self._config.get('proxy')
        if original_proxy is not None:
            if isinstance(original_proxy, dict):
                for key, value in original_proxy.items():
                    self.proxy = { key: value }
            else:
                self.proxy = { 'https': original_proxy }

    def post(self, uri, payload):
        base_uri = '{}{}'.format(self.server, uri)
        data = json.dumps(payload)
        response = requests.post(base_uri, data=data, headers=self.auth_headers, verify=self.verify, proxies=self.proxy)
        return response

    def get(self, uri, payload):
        base_uri = '{}{}'.format(self.server, uri)
        return requests.get(base_uri, params=payload, headers=self.auth_headers, verify=self.verify, proxies=self.proxy)

    @classmethod
    def _get_pk(cls, cef, search_config, fips):
        keys = search_config.get(PKS)
        if sys.version_info >= (3,0):
            if isinstance(keys, str):
                keys = keys.split(',')    
        else:
            if isinstance(keys, basestring):
                keys = keys.split(',')
        if not keys:
            pk_str = ''
            if fips:
                try:
                    pk_hash = hashlib.sha256(json.dumps(cef)).hexdigest()
                except:
                    pk_hash = hashlib.sha256(json.dumps(cef).encode()).hexdigest()
            else:
                try:
                    pk_hash = hashlib.md5(json.dumps(cef)).hexdigest()
                except:
                    pk_hash = hashlib.md5(json.dumps(cef).encode()).hexdigest()
        else:
            pk_str = ', '.join([ '{}:{}'.format(k, ''.join(cef[k])) for k in sorted(keys) if k in cef ] )
            if sys.version_info >= (3,0):
                if fips:
                    pk_hash = hashlib.sha256(pk_str.encode()).hexdigest()
                else:
                    pk_hash = hashlib.md5(pk_str.encode()).hexdigest()
            else:
                if fips:
                    pk_hash = hashlib.sha256(pk_str).hexdigest()
                else:
                    pk_hash = hashlib.md5(pk_str).hexdigest()
        return pk_str, pk_hash

    @classmethod
    def find_patterns(cls, search_results, search):
        cef = {}
        prefixes = search.get('_prefixes', {})
        search_prefix = get_safe(search, '_search', '') + '.'

        search_results = dict([ (k.lower(), v) for k, v in search_results.items() if k ])
        for k, v in search.items():
            if k.startswith('_') and k not in (SEVERITY_KEY, SENSITIVITY_KEY, NAME_OVERRIDE_KEY, '_time'):
                continue
            value = None
            vl = v.lower() if v else ''
            if vl in search_results:
                value = search_results[vl]
            else:
                if v in prefixes:
                    prefix = prefixes[v]
                    name = (prefix + '.' + v).lower()
                    if name in search_results:
                        value = search_results[name]
                    else:
                        name = (search_prefix + v).lower()
                        if name in search_results:
                            value = search_results[name]
            if k == SEVERITY_KEY:
                value = v
            elif k == SENSITIVITY_KEY:
                if v in VALID_SENS:
                    value = v
                elif value not in VALID_SENS:
                    value = DEFAULT_SENS
            elif k == NAME_OVERRIDE_KEY and v:
                if not value:
                    value = 'Field "{}" empty or missing'.format(v)
            if value is not None:
                cef[k] = value

        fips = cls.fips_enabled
        if NAME_OVERRIDE_KEY not in cef:
            pk_str, pk_hash = cls._get_pk(cef, search, fips)
            if pk_str:
                pk_str = '{}: {}'.format(search[NAME_KEY], pk_str)
            else:
                pk_str = search[NAME_KEY]
            cef[NAME_OVERRIDE_KEY] = pk_str
        return cef

    def create_artifacts(self, cef, data, search_config):
        artifacts = []
        cur_cef = deepcopy(cef)
        artifact = {}
        fips = self.fips_enabled
        pk_str, pk_hash = self._get_pk(cef, search_config, fips)
        severity = cur_cef.pop(SEVERITY_KEY, DEFAULT_SEV)
        sens = cur_cef.pop(SENSITIVITY_KEY, DEFAULT_SENS)
        name = cur_cef.pop(NAME_OVERRIDE_KEY, 'NAME_MISSING')
        cleaned = dict([ (k, v) for k, v in data.items() if '.' not in k and not k.startswith('$') ])

        cef_types = dict() # SOARHELP-1232 all cef items should have a data type so that you can see the Contextual Modal in SOAR artifacts
        cef_catch = dict() # catch the cef values that are not present in cur_cef, but present in cleaned data
        for c in cur_cef.keys():
            cef_types[c] = [""]
            cef_catch[c] = cur_cef.get(c)
            if cleaned.get(c) is not None and cef_catch.get(c) is None:
                cef_catch[c] = cleaned.get(c)

        cef_types_update = get_safe(search_config, '_cef_types', {})
        for key, value in cef_types_update.items():
            if value != [None]:
                cef_types[key] = value

        artifact['data'] = cleaned
        artifact['cef'] = cef_catch
        dm = get_safe(search_config, '_search', None)
        if dm is None:
            # it's a saved search
            artifact['label'] = get_safe(search_config, '_artifact_label', 'event')
        else:
            artifact['label'] = get_safe(search_config, '_search', 'event')
        artifact['description'] = '({}) added by Splunk App for SOAR Export'.format(unquote(search_config[NAME_KEY]))
        artifact['name'] = unquote(name)
        artifact['source_data_identifier'] = pk_hash
        artifact['type'] = 'event'
        artifact['severity'] = severity
        artifact['cef_types'] = cef_types
        artifacts.append(artifact)
        return artifacts

    def get_or_create_container(self, artifact, cef, search_config):
        container = {}

        query = {
            '_filter_source_data_identifier': repr(artifact['source_data_identifier']),
            'sort': 'create_time',
            'order': 'desc',
            'page_size': 1,
        }
        response = self.get('/rest/container', query)
        if response.status_code != 200:
            msg = 'Failed to query container on SOAR server. code {} response {!r}'.format(response.status_code, response.text)
            self.logger.error(msg)
            raise Exception(msg)

        j = response.json()
        if j['count'] > 0:
            return False, j['data'][0]['id'], response

        severity = cef.pop(SEVERITY_KEY, DEFAULT_SEV)
        sens = cef.pop(SENSITIVITY_KEY, DEFAULT_SENS)
        container['sensitivity'] = sens
        container['severity'] = severity
        container['name'] = unquote(artifact['name'])
        container['description'] = unquote(artifact['description'])
        container['source_data_identifier'] = artifact['source_data_identifier']
        if search_config.get('_label'):
            container['label'] = search_config.get('_label')
        tags = cef.pop(TAGS_KEY, [])
        container['tags'] = tags

        response = self.post('/rest/container', container)
        message = repr(response.text)
        try:
            message = response.json()['message']
        except:
            pass
        if response.status_code != 200:
            try:
                return False, response.json()['existing_container_id'], response
            except:
                pass
            msg = 'Failed to create container on SOAR server. code: {} response: {}'.format(response.status_code, message)
            if message == 'Severity matching query does not exist.':
                return False, None, message
            self.logger.info(msg)
            raise Exception(msg)

        return True, response.json().get('id'), response

    def post_artifact(self, artifact):
        response = self.post('/rest/artifact', artifact)
        if response.status_code != 200:
            try:
                return False, response.json()['existing_artifact_id'], response, None
            except:
                pass
            msg = 'Failed to create artifact on SOAR server. code {} response {!r}'.format(response.status_code, response.text)
            self.logger.error(msg)
            return False, None, response, None
        container = response.json().get('container_id')
        return True, response.json().get('id'), response, container

    def verify_server(self):
        base_uri = "{}/rest/ph_user?include_automation=true&_filter_token__key='{}'".format(self.server, quote(self.token))
        auth_headers = {'ph-auth-token': self.token }
        try:
            response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        except requests.exceptions.ConnectionError as e:
            url_encoded_token = self.token.replace('=', '%3D').replace('+', '%2B').replace('&', '%26')
            message = str(e).replace(url_encoded_token, "<token>")
            raise Exception(message)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                raise Exception(message)
            response_json = response.json()
            if int(response_json['count']) < 1:
                raise Exception('Token not found')
            name = response_json['data'][0].get('username')
        except:
            base_uri = "{}/rest/asset?_filter_token__key='{}'".format(self.server, quote(self.token))
            response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy)
            if response.status_code != 200:
                raise
            response_json = response.json()
            if int(response_json['count']) < 1:
                raise
            name = response_json['data'][0].get('name')
        
        if self.custom_name == '':
            self.custom_name = '{} ({})'.format(name, self.server)
        self.user = name
        return self.contains(), self.cef_metadata()
  
    def json(self):
        j = {
            'custom_name': self.custom_name,
            'default': self.default,
            'server': self.server,
            'user': self.user,
            'ph-auth-token': self.token,
            'ph_auth_config_id': self.ph_auth_config_id,
            'proxy': '',
            'arrelay': self.arrelay
        }
        if self.proxy is not None:
            j['proxy'] = self.proxy
        return j

    def get_playbooks(self):
        base_uri = "{}/rest/playbook?pretty&page_size=16".format(self.server)
        auth_headers = { 'ph-auth-token': self.token }
        response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                return [], message
            response_json = response.json()
            pages = response_json.get('num_pages')
            playbook_results = []
            for page in range(pages):
                page_uri = "{}&page={}".format(base_uri, page)
                page_response = requests.get(page_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy)
                if page_response.status_code != 200:
                    raise
                page_json = page_response.json()
                playbooks = page_json['data']
                for pb in playbooks:
                    playbook_results.append("{}/{}".format(pb.get('_pretty_scm'), pb.get('name')))
            return playbook_results, None
        except:
            self.logger.error("Error retrieving playbooks for {}".format(self.custom_name))

    def get_severities(self):
        base_uri = "{}/rest/severity?pretty".format(self.server)
        auth_headers = { 'ph-auth-token': self.token }
        response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                self.logger.debug(message)
                return [], message
            response_json = response.json()
            pages = response_json.get('num_pages')
            severity_results = []
            for page in range(pages):
                page_uri = "{}&page={}".format(base_uri, page)
                page_response = requests.get(page_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy)
                if page_response.status_code != 200:
                    raise
                page_json = page_response.json()
                severities = page_json['data']
                for sev in severities:
                    name = sev.get('name', '')
                    name_formatted = name[0].upper() + name[1:]
                    severity_results.append(name_formatted)
            self.logger.debug("Severities found: {severity_results}".format(severity_results=severity_results))
            return severity_results, None
        except:
            self.logger.error("Error retrieving severities for {}".format(self.custom_name))

    def check_severity(self, severity):
        severities, error = self.get_severities()
        severities = [x.lower() for x in severities]
        if severity.lower() in severities:
            return True
        return False

    def update_workbook_template_helper(self, uri, method, data=None):
        auth_headers = { 'ph-auth-token': self.token, 'Connection': 'close' }
        if method == 'GET':
            response = requests.get(uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        elif method == 'POST':
            response = requests.post(uri, json=data, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        elif method == 'DELETE':
            delete_data = {}
            if data:
                delete_data = data
            response = requests.delete(uri, json=delete_data, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                return response.status_code, message
            response_json = response.json()
            return response.status_code, response_json
        except:
            pass

    # Check if there is a linked ID for the workbook_template, then also check to see if there is a matching name -> UPDATE
    # Doesn't exist on this server -> POST
    def update_workbook_template(self, workbook_template_list, key=None):
        success = True
        errors = list()
        if len(workbook_template_list) > 0:
            base_uri = "{}/rest/workbook_template".format(self.server)

            get_all_uri = "{}?page_size=0".format(base_uri)
            status_code, message = self.update_workbook_template_helper(get_all_uri, 'GET')
            message_data = message.get('data')
            all_server_workbooks = {}
            for item in message_data:
                all_server_workbooks[item.get('id')] = unquote(json.loads(json.dumps(item.get('name'))))
            self.logger.debug("Workbooks currently on {}: {}".format(self.server, all_server_workbooks))
            list_workbooks_post = []
            list_workbooks_update = []
            # Check if status is published or deleted, to act accordingly
            for item in workbook_template_list:
                # Try to post it to _originating_server
                _originating_server = item.get('_originating_server', [])
                _workbook_template_id = None
                if isinstance(_originating_server, dict):
                    _originating_server = [_originating_server]
                if _originating_server is not None:
                    _workbook_template_id = [_originating_server[idx] for idx in range(len(_originating_server)) if _originating_server[idx]['ph_auth_config_id'] == self.ph_auth_config_id]
                self.logger.info("Server: {} - {} - {}".format(self.server, item.get('name'), item.get('status')))
                workbook_status = item.get('status')
                if not workbook_status in ['deleted', None]:
                    formatted_item = self.create_post_template(item)
                    # Update
                    message = ''
                    posted = False
                    if _workbook_template_id and len(_workbook_template_id) > 0 and item.get('_original_name') is None:
                        uri = "{}/{}".format(base_uri, _workbook_template_id[0].get('workbook_template_id'))
                        if all_server_workbooks.get(_workbook_template_id[0].get('workbook_template_id')) == item.get('name'):
                            formatted_item['id'] = _workbook_template_id[0].get('workbook_template_id')
                            list_workbooks_update.append(formatted_item)
                        else:
                            # Create new
                            list_workbooks_post.append(formatted_item)
                    else:
                        # Make sure things didn't get out of sync and workbook names exists but doesn't have _originating_server
                        for k, v in all_server_workbooks.items():
                            if v == unquote(formatted_item.get('name', '')):
                                formatted_item['id'] = k
                                list_workbooks_update.append(formatted_item)
                                posted = True
                                break
                        if posted is False:
                            # Create new
                            list_workbooks_post.append(formatted_item)
            batch_size = 100
            # post updated here
            self.logger.debug("Number workbooks to update: {}".format(len(list_workbooks_update)))
            self.logger.debug("Number workbooks to create new: {}".format(len(list_workbooks_post)))
            if len(list_workbooks_update) > 0:
                for i in range(0, len(list_workbooks_update), batch_size):
                    self.logger.debug("   Batch {}: {}".format(i, [{item.get('name'), item.get('id')} for item in list_workbooks_update[i:i+batch_size]]))
                    try:
                        status_code, message = self.update_workbook_template_helper(base_uri, 'POST', list_workbooks_update[i:i+batch_size])
                        for item in range(len(message)):
                            if message[item].get('success') is True:
                                self.logger.info("  {} Update by filtered name - {}:  {}".format(self.server, list_workbooks_update[i+item]['name'], message[item]))
                            else:
                                self.logger.debug("   Failed to post {}. Adding it to create new list".format(list_workbooks_update[i+item]['name']))
                                for k, v in all_server_workbooks.items():
                                    if v == list_workbooks_update[i+item]['name']:
                                        list_workbooks_post.append(list_workbooks_update[i+item])
                                        break

                    except Exception as e:
                        success = False
                        errors.append("Workbook '{}': {}\n".format(list_workbooks_update, e))

            # post all new here
            self.logger.debug("Number workbooks to create new (after updates): {}".format(len(list_workbooks_post)))
            if len(list_workbooks_post) > 0:
                for i in range(0, len(list_workbooks_post), batch_size):
                    self.logger.info("   Batch {}: {}".format(i, [item.get('name') for item in list_workbooks_post[i:i+batch_size]]))
                    try:
                        status_code, message = self.update_workbook_template_helper(base_uri, 'POST', list_workbooks_post[i:i+batch_size])
                        for item in range(len(message)):
                            if message[item].get('success') is True:
                                self.logger.info("  {} Create - {}:  {}".format(self.server, list_workbooks_post[i+item]['name'], message[item]))
                            else:
                                self.logger.error("Could not post '{}' to {}".format(list_workbooks_post[i+item]['name'], self.server))
                                success = False
                                errors.append("Workbook '{}': {}\n".format(list_workbooks_post[i+item]['name'], e))
                    except Exception as e:
                        success = False
                        errors.append("Workbook '{}': {}\n".format(list_workbooks_post, e))

            self.logger.debug("Total workbooks created/updated: {}".format(len(list_workbooks_update)+len(list_workbooks_post)))

        if key:
            # post to config
            self.logger.info("Sending sync confirmation complete")
            return success, errors, "sync_key", key
        return success, errors, None, None

    def update_workbook_template_delete(self, workbook_template_list, key=None):
        success = True
        errors = list()
        if len(workbook_template_list) > 0:
            base_uri = "{}/rest/workbook_template".format(self.server)

            get_all_uri = "{}?page_size=0".format(base_uri)
            status_code, message = self.update_workbook_template_helper(get_all_uri, 'GET')
            message_data = message.get('data')
            all_server_workbooks = {}
            for item in message_data:
                all_server_workbooks[item.get('id')] = unquote(json.loads(json.dumps(item.get('name'))))
            self.logger.debug("Workbooks currently on {}: {}".format(self.server, all_server_workbooks))
            del_id_list = []
            del_name_list = []
            # Check if status is published or deleted, to act accordingly
            for item in workbook_template_list:
                # Try to post it to _originating_server
                _originating_server = item.get('_originating_server', [])
                _workbook_template_id = None
                if isinstance(_originating_server, dict):
                    _originating_server = [_originating_server]
                if _originating_server is not None:
                    _workbook_template_id = [_originating_server[idx] for idx in range(len(_originating_server)) if _originating_server[idx]['ph_auth_config_id'] == self.ph_auth_config_id]
                self.logger.info("Server: {} - {} - {}".format(self.server, item.get('name'), item.get('status')))
                workbook_status = item.get('status')
                if item.get('is_default') is True:
                    success = False
                    errors.append("Workbook '{}': Default workbook cannot be deleted\n".format(item.get('name')))
                elif _workbook_template_id and len(_workbook_template_id) > 0:
                    del_id_list.append(_workbook_template_id[0].get('workbook_template_id'))
                    del_name_list.append(item.get('name'))
                else:
                    name_to_search = item.get('name', '')
                    if item.get('_original_name'):
                        name_to_search = item.get('_original_name')
                    name_to_search = unquote(name_to_search)
                    del_id_list += [del_item for del_item in all_server_workbooks if all_server_workbooks.get(del_item) == name_to_search]
                    del_name_list.append(name_to_search)

            self.logger.debug("Number workbooks to delete: {}".format(len(del_id_list)))
            batch_size = 100
            if del_id_list:
                for i in range(0, len(del_id_list), batch_size):
                    self.logger.debug("   Batch {}: {}".format(i, [item for item in del_id_list[i:i+batch_size]]))
                    try:
                        status_code, message = self.update_workbook_template_helper(base_uri, 'DELETE', data={"ids": del_id_list})
                        for item in range(len(message)):
                            if message[item].get('success') is True:
                                try:
                                    self.logger.info(" {} Delete - {}:  {}".format(self.server, del_name_list[i+item], message[item]))
                                except:
                                    pass
                            elif message[item] != 'Requested item not found':
                                success = False
                                errors.append("Workbook '{}': {}\n".format(del_name_list[i+item], message[item]))
                    except Exception as e:
                        self.logger.error("Could not delete all '{}' to {}".format(del_id_list, self.server))
                        success = False
                        # errors.append("Workbook '{}': {}\n".format(item.get('name'), e))

        if key:
            # post to config
            self.logger.info("Sending sync confirmation complete")
            return success, errors, "sync_key", key
        return success, errors, None, None

    def create_post_template(self, workbook_template):
        workbook_template_phases = workbook_template.get('phases', [])
        phases = []
        workbook_allowed_list = {"name", "description", "is_default", "is_note_required"}
        phase_allowed_list = {"name", "order"}
        task_allowed_list = {"name", "description", "order", "owner", "role", "sla"}
        for ip in workbook_template_phases:
            workbook_template_tasks = ip.get('tasks', [])
            tasks = []
            for it in workbook_template_tasks:
                tmp_task = {k: v for (k, v) in it.items() if v and k in task_allowed_list}
                tmp_task.update(it.get('suggestions'))
                tasks.append(tmp_task)

            tmp_phase = {k: v for (k, v) in ip.items() if k in phase_allowed_list}
            tmp_phase.update({ "tasks": tasks })
            phases.append(tmp_phase)
            
        tmp = {k: v for (k, v) in workbook_template.items() if k in workbook_allowed_list}
        if phases:
            tmp['phases'] = phases

        return tmp

    def get_workbook_template(self, last_sync_keys):
        base_uri = "{}/rest/workbook_template?pretty&page_size=16".format(self.server)
        auth_headers = { 'ph-auth-token': self.token, 'Connection': 'close' }
        response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                return [], message
            response_json = response.json()
            pages = response_json.get('num_pages')
            workbook_template_results = {}
            for page in range(pages):
                page_uri = "{}&page={}".format(base_uri, page)
                page_response = requests.get(page_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy)
                if page_response.status_code != 200:
                    raise
                page_json = page_response.json()
                workbook_templates = page_json['data']
                for wt in workbook_templates:
                    if wt.get('status') is not "deleted":
                        name = wt.get('name')
                        local_existing_names = set(workbook_template_results.keys())
                        all_existing_names = local_existing_names.union(last_sync_keys)
                        if name in local_existing_names:
                            count = 1
                            new_name = "{}_{}".format(name, count)
                            while new_name in all_existing_names:
                                count += 1
                                new_name = "{}_{}".format(name, count)
                            workbook_template_results[new_name] = {"_original_name": name, "prev_state": wt.get('status'), "status": "deleted", "name": new_name, "id": wt.get('id'), "description": wt.get('description', ''), "is_default": wt.get("is_default"), "is_note_required": wt.get('is_note_required'), "phases": []}
                        else:
                            workbook_template_results[name] = {"_originating_server": [{"ph_auth_config_id": self.ph_auth_config_id, "workbook_template_id": wt.get('id')}], "status": wt.get('status'), "name": name, "id": wt.get('id'), "description": wt.get('description', ''), "is_default": wt.get("is_default"), "is_note_required": wt.get('is_note_required'), "phases": []}

            return workbook_template_results, None
        except Exception as e:
            self.logger.error("Error retrieving workbook templates for {}: Error: {}".format(self.custom_name, e))

    def get_workbook_phase_template(self):
        base_uri = "{}/rest/workbook_phase_template?pretty&page_size=16".format(self.server)
        auth_headers = { 'ph-auth-token': self.token, 'Connection': 'close' }
        response = requests.get(base_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy, timeout=15)
        try:
            if response.status_code != 200:
                message = 'Failed'
                try:
                    message = response.json().get('message', message)
                except:
                    pass
                return [], message
            response_json = response.json()
            pages = response_json.get('num_pages')
            results = {}
            for page in range(pages):
                page_uri = "{}&page={}".format(base_uri, page)
                page_response = requests.get(page_uri, headers=auth_headers, verify=self.verify, proxies=self.proxy)
                if page_response.status_code != 200:
                    raise
                page_json = page_response.json()
                workbook_templates = page_json['data']
                for wt in workbook_templates:
                    key = str(wt.get('template'))
                    if results.get(key) is None:
                        results[key] = []
                    cleaned_tasks = []
                    tasks = wt.get('tasks', [])
                    for t in tasks:
                        del t['create_time']
                        del t['modified_time']
                        cleaned_tasks.append(t)
                    results[key].append({"name": wt.get('name'), "template": wt.get('template'), "id": wt.get('id'), "order": wt.get("order"), "sla": wt.get('sla'), "sla_type": wt.get('sla_type'), "tasks": cleaned_tasks})
            return results, None
        except:
            self.logger.error("Error retrieving workbook templates for {}".format(self.custom_name))
