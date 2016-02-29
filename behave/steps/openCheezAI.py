import os
import sys
import logging

# Fix for the path...
FILE_DIR = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.join(FILE_DIR, '../../maikosite')
sys.path.insert(0, PROJECT_ROOT_DIR)

from behave import given, then
from utils.openCheezAI import openCheezAICaller

_LOGGER = logging.getLogger('test')
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
_LOGGER.setLevel(logging.DEBUG)

@given(u"person {uin} is reset in openCheezAI")
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
    # retrieve person from openCheezAI
    c = openCheezAICaller()
    person = c.get_person_by_uin(uin)

    # check attributes
    for row in context.table:
        attr = row['attr']
        value = row['value']
        assert attr in person, "Has key %s." % attr
        assert (person[attr] == value), "%s == %s" % (attr, value)


@then(u'person {uin} has {attr} set to {value} in openCheezAI')
def has_openCheezAI_value(context, uin, attr, value):

    # retrieve person from openCheezAI
    c = openCheezAICaller()
    person = c.get_person_by_uin(uin)

    assert attr in person, "Has key %s." % attr
    assert (person[attr] == value), "%s == %s" % (attr, value)
#====

