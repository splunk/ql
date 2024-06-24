import os
from urllib.parse import quote_plus
import json
import requests

# from splunk.clilib.bundle_paths import make_splunkhome_path
from splunk import setupSplunkLogger, ResourceNotFound
import splunk.rest as rest

APP_HOME_DIR = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps', 'phantom')

def get_search_description(helper, search_name):
    path = f'/services/saved/searches/{quote_plus(search_name)}'
    try:
        response, contents = script_rest_helper(helper, helper.settings.get('session_key'), 'GET', path)
        if 200 <= int(response.get('status')) < 300:
            json_content = json.loads(contents)
            entries = json_content.get('entry')
            for item in entries:
                if item.get('name', '') == search_name:
                    search_description = item.get('content', {}).get('description', '')
                    return search_description
    except Exception as e:
        pass
    return None

def script_rest_helper(logger, session_key, method, path, payload={}):
    try:
        args = {
            'method': method,
            'sessionKey': session_key
        }
        payload['output_mode'] = 'json'
        if method == 'POST' or method == 'DELETE':
            args['postargs'] = payload
        else:
            args['getargs'] = payload
        response, contents = rest.simpleRequest(path, **args)
    except ResourceNotFound as e:
        # Not raising this error purposefully
        raise ResourceNotFound("ResourceNotFound: {}".format(str(e)))
    except Exception as e:
        # Not raising this error purposefully
        raise Exception("Exception: {}".format(str(e)))
    return response, contents

def rest_helper(logger, credentials, method, path, payload={}):
    try:
        request_func = getattr(requests, method)
    except AttributeError:
        return False, "Invalid method: {method}".format(method=method)

    r = None
    try:
        r = request_func(path,
                        auth=credentials,
                        headers={ 'Content-Type': 'application/json' },
                        verify=False)
    except Exception as e:
        return False, "Error: {}".format(e)

    try:
        return True, r.json()
    except Exception as e:
        return False, "Error: Could not parse json"
