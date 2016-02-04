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
    TemplateView based SOAP view
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
        Just print the desired function call for now.
        '''
        _LOGGER.debug("in post method")

        try:
            # Logic here
            function, args = soap_string_to_function_call(request.body)
            _LOGGER.debug("calling SOAP parse now")

#           return (render_to_response('openCheezAI/function.html', 
#                                 {'function_call' : function},
#                                 content_type='application/xml'
#                                 ))

            _LOGGER.debug("in post, got function %s " % (function))

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
                                  content_type='application/xml'
                                  ))

                except Person.DoesNotExist as e:
                    return (render_to_response(
                              'openCheezAI/get_netid_assignment_not_found.xml',
                                  {},
                                  content_type='application/xml'
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
                              content_type='application/xml'
                              ))

#           # GetBasicPerson(UIN)
#           elif function == 'GetBasicPerson':
#               uin = args[0]
#
#           # GetInstitutionalIdentity(UIN)
#           elif function == 'GetInstitutionalIdentity':
#               uin = args[0]
#
#           # AssignNetid(UIN, campus.edu)
#           elif function == 'AssignNetid':
#               uin = args[0]
#               campus = args[1]
#               campus = campus[0:-4] # remove trailing ".edu"

            # Anything else, we error out.
            else:
                raise Exception("Didn't get a good function")
                #return(HttpResponseServerError)

        except Exception as e:
            raise Exception("something barfed:" + e.message)
            # Default, return 500
            #return(HttpResponseServerError)


#       # self.request.session['foo'] = "bar"
#       function_call = soapStringToFunctionCall(request.body)
#       self.request.session['function_call'] = function_call
#       return (render_to_response('openCheezAI/function.html', 
#                                 {'function_call' : function_call},
#                                 content_type='application/xml'
#                                 ))
 
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

def soapStringToFunctionCallString(soapString):
    
    if not soapString:
        return "No function called."
    # Create tree.

    tree = ET.ElementTree(ET.fromstring(soapString))

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

    # Args are the children of the function, they are anonymous args
    args = [arg.text for arg in function.getchildren()]

    # Print the results!
    args.insert(0, function_name)

    return ' '.join(args)

