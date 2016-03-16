import os
import sys
import logging

# Fix for the path...
FILE_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.join(FILE_DIR, '../../maikosite')
sys.path.insert(0, PROJECT_ROOT_DIR)

from behave import given, when, then
from utils.openCheezAI import openCheezAICaller
import requests
from requests.auth import HTTPBasicAuth

import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger('test')
logging.basicConfig(filename='debug.log', filemode='w', level=logging.WARN)
_LOGGER.setLevel(logging.WARN)

def _call_getNetIDForUINAL(querystring_hash):
    '''
    Calls getNetIDForUINAL with the querystring arguments given in the hash.
    Returns a hash of returned values.
    Extra key "status" is populated with "success" or "error"
    '''

    #Hardcoded configuration for calling CDUS right now
    user = 'citessdg'
    password = 'pHi.4075'
    getNetIDForUINAL_URL = 'https://directory-dev.techservices.illinois.edu:4443/cdus/getNetIDForUIN' 

    # Call it!
    resp = requests.get(getNetIDForUINAL_URL, params=querystring_hash, 
                        auth=HTTPBasicAuth(user, password)) 
    resp.raise_for_status()

    # Parse out the results. 
    tree = ET.ElementTree(ET.fromstring(resp.content))
    root = tree.getroot()

    if root.tag == 'getNetIDForUIN':
        return { 
          'status' : 'success',
          'suggestedNetID' : root.findtext('suggestedNetID'),
          'netIDSource' : root.findtext('netIDSource'),
          'uinFoundInCentralRegistry' : root.findtext('uinFoundInCentralRegistry'),
          'needRegisterAtUIUC' : root.findtext('needRegisterAtUIUC'),
          'needRegisterAtIllinois' : root.findtext('needRegisterAtIllinois'),
          'needRegisterAtUillinois' : root.findtext('needRegisterAtUillinois'),
        }

    elif root.tag == 'error':
        return { 
            'status' : 'error',
            'code' : root.findtext('code'),
            'string' : root.findtext('string'),
            'detail' : root.findtext('detail'),
        }
    return {}


@when(u"getNetIDForUINAL is called with arguments")
def call_getNetIDForUINAL(context):
    query_string_hash = {}
    for row in context.table:
        attr = row['attr']
        value = row['value']
        query_string_hash[attr] = value

    results = _call_getNetIDForUINAL(query_string_hash)
    context.getNetIDForUINAL_results = results

     
@then(u'getNetIDForUINAL succeeds with results')
def confirm_getNetIDForUINAL_success_result(context):
    # get results off context 
    results = context.getNetIDForUINAL_results
    
    # check attributes of result
    assert results['status'] == 'success', 'getNetIDForUINAL returned success.'
    for row in context.table:
        attr = row['attr']
        value = row['value']
        assert (results[attr] == value), "%s == %s" % (attr, value)



@then(u'getNetIDForUINAL fails with error code {code}')
def confirm_getNetIDForUINAL_error_result(context, code):
    # get results off context 
    results = context.getNetIDForUINAL_results

    # check attributes of result
    assert results['status'] == 'error', 'getNetIDForUINAL returned error.'
    assert results['code'] == code, "Error code was %s" % code

