import logging
import os
from ConfigParser import RawConfigParser

# ===================
# Setup Logging 
# ===================
_LOGGER = logging.getLogger("test")
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())

_SETTINGS_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEST_CONF_FILE = os.path.join(_SETTINGS_LOCATION, 'test.conf')
_LOGGER.info('Test config file: %s', TEST_CONF_FILE)

config = RawConfigParser()
config.read(TEST_CONF_FILE)

CR_LDAP_CONFIG = {
    'uri': config.get('ldap', 'LDAP_URL'),
    'base_dn': config.get('ldap', 'LDAP_SEARCH_BASE'),
    'bind_dn': config.get('ldap', 'LDAP_USER'),
    'password': config.get('ldap', 'LDAP_USER_PASSWORD'),
}

TEST_NETID = 'testnetid'
DEFAULT_ATTRS = {
'cn':TEST_NETID,
'displayName':'Plain T. User',
'eduPersonPrincipalName':TEST_NETID,
'givenName':'Plain',
'objectclass':['top','person','organizationalPerson','inetOrgPerson', 'uiucEduPerson'],
'sn':'User',
'uid':'a07e461ccc4d1f32022fafa8894f9430',
'uiucEduAffiliation':['person','phone',],
'uiucEduFirstName':'Plain',
'uiucEduLastName':'User',
'uiucEduMiddleName':'T',
'uiucEduNetID':TEST_NETID,
'uiucEduRegistryCreateDate':'20090531120000',
'uiucEduRegistryModifyDate':'20101231004800',
'uiucEduType':['person','phone'],
'uiucEduUIN':'652999444',
'uiucEduUnixUID':'119109',
}
