'''
Copyright (C) 2005-2012 Splunk Inc. All Rights Reserved.
'''
import shutil
from splunk.models.base import SplunkAppObjModel
from splunk.models.field import Field
import splunk 
import splunk.rest as rest
from splunk.clilib.bundle_paths import make_splunkhome_path
from lookup_editor.shortcuts import escape_filename

import os
import sys
import shutil
import tempfile
import time

class SplunkLookupTableFile(SplunkAppObjModel):
    '''Class for Splunk lookup table files.
    
    Note that on save(), the "path" is actually
    the file that will be copied into place to replace the existing lookup
    table.
    '''

    resource = '/data/lookup-table-files'
    name = Field()
    path = Field(api_name="eai:data")
    
    @staticmethod
    def reload( session_key=None ):
        path = SplunkLookupTableFile.resource + "/" + '_reload'
        
        response, _ = rest.simpleRequest(path, method='GET', sessionKey=session_key)
        if response.status == 200:
            return True
        
        return False

class SplunkTransformLookup(SplunkAppObjModel):
    '''Class for Splunk lookups as defined in transforms.conf.'''

    resource = '/data/transforms/lookups'
    name = Field()
    filename = Field()

class Errors:
    ERR_NO_LOOKUP         = "Lookup file was not found"
    ERR_UNKNOWN_EXCEPTION = "Unexpected exception"

def get_lookup_table_location(lookup_name, namespace, owner, key, fullpath=True):
    '''Retrieve the location of a Splunk lookup table file by lookup name.
    
    @param lookup_name: The lookup STANZA name (NOT the file name).
    @param namespace: A Splunk namespace to limit the search to.
    @param owner: A Splunk user.
    @param key: A Splunk session key.
    @param fullpath: Return full path if True, file name alone if False.
    
    @return: The path to the Splunk lookup table.
    '''
    try:
        transform = SplunkTransformLookup.get(SplunkTransformLookup.build_id(lookup_name, namespace, owner), sessionKey=key)
        path = SplunkLookupTableFile.get(SplunkLookupTableFile.build_id(transform.filename, namespace, owner), sessionKey=key).path
        if not fullpath:
            return os.path.basename(path)
        return path
    except splunk.ResourceNotFound as e:
        sys.stderr.write(Errors.ERR_NO_LOOKUP + ': %s\n' % str(e))
        pass
    except Exception as e:
        sys.stderr.write(Errors.ERR_UNKNOWN_EXCEPTION + ': %s\n' % str(e))
        pass

def create_lookup_table(filename, lookup_file, namespace, owner, key):
    '''
    Create a new lookup file.

    @param filename: The full path to the replacement lookup table file.
    @param lookup_file: The lookup FILE name (NOT the stanza name)
    @param namespace: A Splunk namespace to limit the search to.
    @param owner: A Splunk user.
    @param key: A Splunk session key.
    
    @return: Boolean success status.
    
    WARNING: "owner" should be "nobody" to update
    a public lookup table file; otherwise the file will be replicated
    only for the admin user.
    '''
    
    # Create the temporary location path
    lookup_tmp = make_splunkhome_path(['var', 'run', 'splunk', 'lookup_tmp'])
    destination_lookup_full_path = os.path.join(lookup_tmp, lookup_file)

    # Copy the file to the temporary location
    shutil.move(filename, destination_lookup_full_path)

    # CReate the URL for the REST call
    url = '/servicesNS/%s/%s/data/lookup-table-files' % (owner, namespace)
    postargs = {
        'output_mode': 'json',
        'eai:data': str(destination_lookup_full_path),
        'name': lookup_file
    }

    # Perform the call
    rest.simpleRequest(
         url, postargs=postargs, sessionKey=key, raiseAllErrors=True)

def update_lookup_table(filename, lookup_file, namespace, owner, key):
    '''Update a Splunk lookup table file with a new file.
    
    @param filename: The full path to the replacement lookup table file.
    @param lookup_file: The lookup FILE name (NOT the stanza name)
    @param namespace: A Splunk namespace to limit the search to.
    @param owner: A Splunk user.
    @param key: A Splunk session key.
    
    @return: Boolean success status.
    
    WARNING: "owner" should be "nobody" to update
    a public lookup table file; otherwise the file will be replicated
    only for the admin user.
    '''
    
    # Create the temporary location path
    lookup_tmp = make_splunkhome_path(['var', 'run', 'splunk', 'lookup_tmp'])
    destination_lookup_full_path = os.path.join(lookup_tmp, lookup_file)

    # Copy the file to the temporary location
    shutil.move(filename, destination_lookup_full_path)

    # CReate the URL for the REST call
    url = '/servicesNS/%s/%s/data/lookup-table-files/%s' % (owner, namespace, lookup_file)
    postargs = {
        'output_mode': 'json',
        'eai:data': str(destination_lookup_full_path)
    }

    # Perform the call
    rest.simpleRequest(
         url, postargs=postargs, sessionKey=key, raiseAllErrors=True)

def get_temporary_lookup_file(prefix=None, basedir=None):
    '''Create a temporary file and return the filehandle.
    Exceptions will be passed to caller.

    @param prefix: A prefix for the file (default is "lookup_gen_<date>_<time>_")
    @param basedir: The base directory for the file (default is $SPLUNK_HOME/var/run/splunk/lookup_tmp,
        the staging directory for use in creating new lookup table files).
    '''
    
    if prefix is None:
        prefix = 'lookup_gen_' + time.strftime('%Y%m%d_%H%M%S') + '_'
    
    if basedir is None:
        basedir = make_splunkhome_path(['var', 'run', 'splunk', 'lookup_tmp'])

    if not os.path.isdir(basedir):
        os.mkdir(basedir)

    if os.path.isdir(basedir):
        return tempfile.NamedTemporaryFile(prefix=prefix,
            suffix='.txt',
            mode='w+',
            dir=basedir,
            encoding="utf-8",
            delete=False)
    else:
        return None
    
#   Sample usage
#    src_lookup_path = get_lookup_table_location(options.src_lookup_name, options.namespace, options.owner, sessionKey)
#    success = update_lookup_table(tempfile, tgt_lookup_path, options.namespace, options.owner, sessionKey)
