import os
import sys
import logging

# Fix for the path...
FILE_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.join(FILE_DIR, '../../maikosite')
sys.path.insert(0, PROJECT_ROOT_DIR)

from behave import given, then
from utils.openCheezAI import openCheezAICaller

@given(u"person '{uin}' is reset in openCheezAI")
def reset_person(context, uin):
    # clear out person from openCheezAI
    c = openCheezAICaller()
    c.delete_person(uin)

    # make new blank person on context
    context.person = c.get_blank_person_template()
    context.person['uin'] = uin


@given(u'person has openCheezAI attribute values')
def openCheezAI_attrs(context):
    for row in context.table:
        attr = row['attr']
        value = row['value']
        attr = attr.encode('ascii', 'ignore')
        value = value.encode('ascii', 'ignore')
        context.person[attr] = value


@given(u'person exists in openCheezAI')
def add_to_openCheezAI(context):
    # add the person in the context to the openCheezAI
    c = openCheezAICaller()
    c.create_person(context.person['uin'], context.person)

@then(u'person {uin} exists in openCheezAI with attribute values')
def confirm_openCheezAI_attrs(context, uin):
    # clear out person from openCheezAI
    c = openCheezAICaller()
    person = c.get_person_by_uin(uin)

    for row in context.table:
        attr = row['attr']
        value = row['value']
        attr = attr.encode('ascii', 'ignore')
        value = value.encode('ascii', 'ignore')
        context.person[attr] = value

@then('person {uin} has {attr} set to {value} in openCheezAI')
def has_openCheezAI_value(context, uin, attr, value):

#====

@then('user has {attr} set to {value} in Central Registry')
def has_central_registry_value(context, attr, value):
    attr = attr.encode('ascii', 'ignore')
    value = value.encode('ascii', 'ignore')

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
