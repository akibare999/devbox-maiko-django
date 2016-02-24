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

