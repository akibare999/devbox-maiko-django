import os
import sys
import logging

# Fix for the path...
FILE_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.join(FILE_DIR, '../../maikosite')
sys.path.insert(0, PROJECT_ROOT_DIR)

from behave import given, then
from utils.openCheezAI import openCheezAICaller
import requests
from requests.auth import HTTPBasicAuth

import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger('test')
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
_LOGGER.setLevel(logging.DEBUG)

def _call_getNetIDForUINAL(querystring_hash):
    '''
    Calls getNetIDForUINAL with the querystring arguments given in the hash.
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
          'suggestedNetID' : root.findtext('suggestedNetID'),
          'netIDSource' : root.findtext('netIDSource'),
          'uinFoundInCentralRegistry' : root.findtext('uinFoundInCentralRegistry'),
          'needRegisterAtUIUC' : root.findtext('needRegisterAtUIUC'),
          'needRegisterAtIllinois' : root.findtext('needRegisterAtIllinois'),
          'needRegisterAtUillinois' : root.findtext('needRegisterAtUillinois'),
        }

    elif root.tag == 'error':
        return { 
            'code' : root.findtext('code'),
            'string' : root.findtext('string'),
            'detail' : root.findtext('detail'),
        }
    return {}


### MAIN ###

qsh = { 'firstName':'Jon', 
        'lastName':'Roma', 
        'uin':'652974446',
      }

results = _call_getNetIDForUINAL(qsh)

print "Results for Jon:"
print "---------------------------------------------------------------------"
for key in results:
    print "%s ===> %s" % (key, results[key])
print "---------------------------------------------------------------------"
print

qsh = { 'firstName':'Jon', 
        'lastName':'Roma', 
      }

results = _call_getNetIDForUINAL(qsh)

print "Error for missing UIN:"
print "---------------------------------------------------------------------"
for key in results:
    print "%s ===> %s" % (key, results[key])
print "---------------------------------------------------------------------"

