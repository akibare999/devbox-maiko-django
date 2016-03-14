# Common library imports
import os
import sys
import ldap
import ldap.modlist
import logging
import random
from behave import given, then

# Fix for the path...
FILE_DIR = os.path.dirname(__file__)
# TODO: Edited location of project root dir
PROJECT_ROOT_DIR = os.path.join(FILE_DIR, '../../maikosite')
BEHAVE_ROOT_DIR = os.path.join(FILE_DIR, '..')
sys.path.insert(0, PROJECT_ROOT_DIR)
sys.path.insert(0, BEHAVE_ROOT_DIR)

# SDG Team imports 
# from test.selenium.sdg.directory import DirectoryConnection
from sdg.directory import CampusLDAPConnection 

# App imports
# from main import settings
from test_settings import DEFAULT_ATTRS
# from test_settings import DEFAULT_ATTRS, TEST_NETID
import test_settings as settings

_LOGGER = logging.getLogger('test')
# _LOGGER.setLevel(logging.INFO)
_LOGGER.setLevel(logging.DEBUG)

# ===================
# Handlers
# ===================

def _get_random_dn():
    random_number = random.randrange(11,99)
    return "uid=227f043a83c3f3e1cf2d43ce21354d%s,ou=people,DC=UIUC,DC=EDU" % random_number

def _get_cr_conn():
    ''' Get a connection to the central registy. '''
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    # conn = DirectoryConnection(**settings.CR_LDAP_CONFIG)
    conn = CampusLDAPConnection(**settings.CR_LDAP_CONFIG)
    # print("Connection info: {}".format(settings.CR_LDAP_CONFIG))
    return conn

def _reset_user(netid, context):
    ''' Remove the user from Central Registry, if they exist.
    Start a replacement record on the context, to be added later.
    '''
    conn = _get_cr_conn()
    result = conn.lookup_by_netid(netid)

    if result:
        _LOGGER.info("Cleaning up %s existing entries.", len(result))
        for entry in result:
            #_LOGGER.info("Cleaning up entry: {}".format(str(entry)))
            dn, _ = entry
            # _LOGGER.info("The rest: {}".format(str(the_rest)))
            _LOGGER.info("Removing %s from CR.", dn)
            result = conn.connection.delete_s(dn)
            # Behave swallows the last log output...
            # _LOGGER.info("Remove Result: {}".format(result))
            # _LOGGER.info("Removed {} from CR.".format(dn))
            # _LOGGER.info("Behave log swallog bug gone?")
    else:
        _LOGGER.info("No entries in CR match config file NetID")

    context.attrs = DEFAULT_ATTRS
    context.dn = _get_random_dn()
    context.net_id = netid
    set_attr_value(context, attr='uiucEduNetID', value=netid)
    set_attr_value(context, attr='eduPersonPrincipalName', value=netid)
    set_attr_value(context, attr='cn', value=netid)
    _LOGGER.debug("Attributes: %s", context.attrs)

@given(u"user '{netid}' is reset in Central Registry")
def reset_netid_user(context, netid):
    _reset_user(netid, context)

#@given(u'user from config file is reset in Central Registry')
#def reset_user(context):
#    _reset_user(TEST_NETID, context)

@given('user has {attr} set to {value}')
def set_attr_value(context, value, attr):
    ''' For single value attributes. '''
    attr = attr.encode('ascii', 'ignore')
    value = value.encode('ascii', 'ignore')
    context.attrs[attr] = value

@given(u'user has Central Registry attribute values')
def cr_single_attrs(context):
    for row in context.table:
        attr = row['attr']
        value = row['value']
        attr = attr.encode('ascii', 'ignore')
        value = value.encode('ascii', 'ignore')
        context.attrs[attr] = value

@given('user has {value} in {attr}')
def add_value_to_attr(context, value, attr):
    ''' For attributes that are lists. '''
    # The directory does not want unicode.
    attr = attr.encode('ascii', 'ignore')
    value = value.encode('ascii', 'ignore')
    # Add the key if not already there.
    if not attr in context.attrs:
        context.attrs[attr] = []
    # Add the value
    if not value in context.attrs[attr]:
        context.attrs[attr].append(value)

@given('user exists in Central Registry')
def add_to_central_registy(context):
    conn = _get_cr_conn()
    try:
        conn.connection.delete_s(context.dn)
        _LOGGER.info("Deleted CR user %s" % context.dn)
    except ldap.NO_SUCH_OBJECT:
        _LOGGER.debug("Already gone. Skip delete.")
    modList = ldap.modlist.addModlist(context.attrs)
    # print("Modlist: {}".format(modList))
    conn.connection.add_s(context.dn, modList)
    # print("Hooray!")
    _LOGGER.info("Recreated user: %s", context.dn)
    # _LOGGER.debug("Attributes: {}".format(context.attrs))


@then('user has {attr} set to {value} in Central Registry')
def has_central_registry_value(context, attr, value):
    attr = attr.encode('ascii', 'ignore')
    value = value.encode('ascii', 'ignore')
    # _LOGGER.debug("Called with attr '{}' and value '{}'".format(attr, value))

    conn = _get_cr_conn()
    kwargs = {
        # 'ldap_filter':'dn={}'.format(context.dn),
        'ldap_filter':'uiucEduNetID=%s' % context.net_id,
        'attr_list':[attr],
    }
    # _LOGGER.debug("LDAP lookup args: {}".format(kwargs))
    result = conn.lookup(**kwargs)
    # assert len(result) == 1, "{} results.".format(len(result))
    record = result[0]
    # _LOGGER.debug("CR Lookup result: {}".format(result))
    assert attr in record, "Has key %s." % attr
    assert (record[attr] == value), "%s == %s" % (attr, value)

