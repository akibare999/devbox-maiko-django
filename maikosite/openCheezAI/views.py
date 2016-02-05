from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, View

from openCheezAI.models import Person
from openCheezAI.serializers import PersonSerializer

from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from django.http import HttpResponse, HttpResponseServerError

import xml.etree.ElementTree as ET
import re
import logging
import datetime

_LOGGER = logging.getLogger(__name__)


# Create your views here.

#-------------------------------------------------------------------------------
# REST VIEWS
#-------------------------------------------------------------------------------

class PersonList(generics.ListCreateAPIView):
    '''
    List all Person objects, or create a new Person object.
    '''
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update, or delete a Person instance.
    '''
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'persons': reverse('person-list', request=request, format=format),
    })

#-------------------------------------------------------------------------------
# CHEEZY SOAP VIEWS
#-------------------------------------------------------------------------------

class SoapHandlerView(View):
    '''
    Generic View based SOAP view. Accept POST only, return XML.
    '''
    http_method_names = ['post']

    template_name = "openCheezAI/function.html"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        '''
        Turn off CSRF because we're using this for an API (post only).
        '''
        return super(SoapHandlerView, self).dispatch(request, *args, **kwargs)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        '''
        (1) Parse the incoming SOAP (request.body) into a function call
        (2) Implement a version of the call against the openCheezAI db
            (Person objects)
        (3) Return a precooked "SOAP" xml template with the relevant
            values filled in from the Person fields.
        '''

        try:
            # Parse the incoming soap to get a [function, [args]]
            function, args = soap_string_to_function_call(request.body)

            # GetNetidAssignment(UIN)
            if function == 'GetNetidAssignment':
                uin = args[0]
                try:
                    p = Person.objects.get(uin=uin)
                    local_context = {}
                    if (p.uillinois_netid):
                        local_context['uillinois_netid'] = '<uillinois.edu>' +\
                                     p.uillinois_netid + '</uillinois.edu>'
                    if (p.illinois_netid):
                        local_context['illinois_netid'] = '<illinois.edu>' +\
                                     p.illinois_netid + '</illinois.edu>'
                    if (p.uiuc_netid):
                        local_context['uiuc_netid'] = '<uiuc.edu>' +\
                                     p.uiuc_netid + '</uiuc.edu>'
                    if (p.uic_netid):
                        local_context['uic_netid'] = '<uic.edu>' +\
                                     p.uic_netid + '</uic.edu>'
                    if (p.uis_netid):
                        local_context['uis_netid'] = '<uis.edu>' +\
                                     p.uis_netid + '</uis.edu>'
                    return (render_to_response(
                              'openCheezAI/get_netid_assignment.xml',
                                  local_context,
                                  content_type='text/xml; charset=UTF-8'
                                  ))

                except Person.DoesNotExist as e:
                    return (render_to_response(
                              'openCheezAI/get_netid_assignment_not_found.xml',
                                  {},
                                  content_type='text/xml; charset=UTF-8'
                                  ))

            # NetidInUse(NetID)
            elif function == 'NetidInUse':
                netid = args[0]
                netid_in_use = 0
                people =  Person.objects.filter(uillinois_netid=netid)
                people |=  Person.objects.filter(illinois_netid=netid)
                people |=  Person.objects.filter(uiuc_netid=netid)
                people |=  Person.objects.filter(uic_netid=netid)
                people |=  Person.objects.filter(uis_netid=netid)
                if people:
                    netid_in_use = 1
                return (render_to_response(
                          'openCheezAI/netid_in_use.xml',
                              {'netid_in_use': netid_in_use},
                              content_type='text/xml; charset=UTF-8'
                              ))

            # GetBasicPerson(UIN)
            elif function == 'GetBasicPerson':
                uin = args[0]
                try:
                    p = Person.objects.get(uin=uin)
                    local_context = {}
                    # TODO: Add banner_middlename to Person model
                    local_context['banner_middlename'] = 'X'
                    local_context['banner_firstname'] = p.banner_firstname
                    local_context['banner_lastname'] = p.banner_lastname
                    if p.banner_suppressed:
                        local_context['banner_suppressed'] = \
                        '<confidential xsi:type="xsd:string">Y</confidential>'

                    return (render_to_response(
                              'openCheezAI/get_basic_person.xml',
                                  local_context,
                                  content_type='text/xml; charset=UTF-8'
                                  ))

                except Person.DoesNotExist as e:
                    # Banner SOAP call returns a 500 for Not Found,
                    # so we mimic this (less than great!) behavior
                    raise Exception("No Basic Person Found for UIN %s " %
                                     uin)

            # GetInstitutionalIdentity(UIN)
            elif function == 'GetInstitutionalIdentity':
                uin = args[0]
                try:
                    p = Person.objects.get(uin=uin)
                    local_context = {}
                    # TODO: Add i2s_middlename to Person model
                    local_context['i2s_middlename'] = 'X'
                    local_context['i2s_firstname'] = p.banner_firstname
                    local_context['i2s_lastname'] = p.banner_lastname

                    return (render_to_response(
                              'openCheezAI/get_institutional_identity.xml',
                                  local_context,
                                  content_type='text/xml; charset=UTF-8'
                                  ))

                except Person.DoesNotExist as e:
                    # GetInstitutionalIdentity SOAP call returns a 500 for Not 
                    # Found, so we mimic this (less than great!) behavior
                    raise Exception("No InstitutionalIdentity Found for \
                                     UIN %s " % uin)
 
            # AssignNetid(UIN, campus.edu)
            # TODO: Check the actual return XML for this (in dev or somewhere)
            elif function == 'AssignNetid':
                uin = args[0]
                netid = args[1]
                campus = args[2]
                try:
                    p = Person.objects.get(uin=uin)
                except Person.DoesNotExist as e:
                        # Can't set netid for non-existent user
                        raise Exception("No user found with uin %s" % uin)

                if campus == 'uillinois.edu':
                    # Make sure that there is no conflict in assignment.
                    conflicts =  Person.objects.filter(uillinois_netid=netid)
                    if conflicts:
                        raise Exception("netid %s already assigned at \
                              uillinois.edu to UIN %s" % (netid, uin))
                    try:
                        p.uillinois_netid = netid
                        p.save()
                    except Exception as e:
                        # Something went wrong in set
                        raise Exception("Unable to assign netid %s to \
                                        uin %s for uillinois.edu: %s" %
                                        (netid, uin, str(e)))
                        
                elif campus == 'illinois.edu':
                    # Make sure that there is no conflict in assignment.
                    conflicts =  Person.objects.filter(illinois_netid=netid)
                    if conflicts:
                        raise Exception("netid %s already assigned at \
                              illinois.edu to UIN %s" % (netid, uin))
                    try:
                        p.illinois_netid = netid
                        p.save()
                    except Exception as e:
                        # Something went wrong in set
                        raise Exception("Unable to assign netid %s to \
                                        uin %s for illinois.edu: %s" %
                                        (netid, uin, str(e)))
                        
                elif campus == 'uiuc.edu':
                    # Make sure that there is no conflict in assignment.
                    conflicts =  Person.objects.filter(uiuc_netid=netid)
                    if conflicts:
                        raise Exception("netid %s already assigned at \
                              uiuc.edu to UIN %s" % (netid, uin))
                    try:
                        p.uiuc_netid = netid
                        p.save()
                    except Exception as e:
                        # Something went wrong in set
                        raise Exception("Unable to assign netid %s to \
                                        uin %s for uiuc.edu: %s" %
                                        (netid, uin, str(e)))
                        
                elif campus == 'uic.edu':
                    # Make sure that there is no conflict in assignment.
                    conflicts =  Person.objects.filter(uic_netid=netid)
                    if conflicts:
                        raise Exception("netid %s already assigned at \
                              uic.edu to UIN %s" % (netid, uin))
                    try:
                        p.uic_netid = netid
                        p.save()
                    except Exception as e:
                        # Something went wrong in set
                        raise Exception("Unable to assign netid %s to \
                                        uin %s for uic.edu: %s" %
                                        (netid, uin, str(e)))
                        
                elif campus == 'uis.edu':
                    # Make sure that there is no conflict in assignment.
                    conflicts =  Person.objects.filter(uis_netid=netid)
                    if conflicts:
                        raise Exception("netid %s already assigned at \
                              uis.edu to UIN %s" % (netid, uin))
                    try:
                        p.uis_netid = netid
                        p.save()
                    except Exception as e:
                        # Something went wrong in set
                        raise Exception("Unable to assign netid %s to \
                                        uin %s for uis.edu: %s" %
                                        (netid, uin, str(e)))
                        
                else:
                    raise Exception("Unable to assign netid %s to \
                                    uin %s for unknown campus %s" %
                                    (netid, uin, campus))

                # If everything went ok, return generic XML response.
                return(render_to_response(
                          'openCheezAI/assign_netid.xml',
                           {},
                           content_type='text/xml; charset=UTF-8'
                           ))

            # Anything else, we error out.
            else:
                raise Exception("Unknown function %s sent to openCheezAI \
                                SOAP" % function)

        except Exception as e:
            raise Exception("openCheezAI SOAP failure: " + e.message)
 
#-------------------------------------------------------------------------------
# UTILITY FUNCTIONS
#-------------------------------------------------------------------------------

def soap_string_to_function_call(soap_string):
    '''
    Converts the SOAP received from TDI into a "function call" 
    we can take action on.
    Arguments:
        (1) soapString - full BODY of the POST request received
    Returns:
        (1) List: [ function [ args] ] 
    Throws:
        Any kind of exceptions - we catch general exceptions in the
        caller and raise a 500 from there.

    '''
    
    if not soap_string:
        return ['no_function',[]]

    # Create tree.

    tree = ET.ElementTree(ET.fromstring(soap_string))

    root = tree.getroot()

    # Can find the body directly because we know the namespace
    # won't change, so just hardcode it
    body = root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')

    # Function is the singleton child of the body, always
    # Kill the namespace because we don't care about it and it 
    # changes based on server.
    function = body.getchildren()[0]
    function_name = function.tag
    function_name = re.sub('{.*}','',function_name)
    _LOGGER.debug("IN PARSER: function is: %s" % function_name)

    # Args are the children of the function, they are anonymous args
    args = [arg.text for arg in function.getchildren()]

    return [function_name, args]

