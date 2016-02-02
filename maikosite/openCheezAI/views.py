from django.shortcuts import render

from openCheezAI.models import Person
from openCheezAI.serializers import PersonSerializer

from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from django.http import HttpResponse

import xml.etree.ElementTree as ET
import re

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

# Make a cheesy functional view so that no CSRF is required but also 
# no serializer required because this is cheez.
# Question: Would there be some way to build the soapStringToFunction
# thingy into a serializer? 

@api_view(['POST'])
def soap_handler_view(request, format=None):
    '''
    Just print crud for now...
    '''
    if request.method == 'POST':
        function_call = soapStringToFunctionCall(request.body)
        return HttpResponse('you called SOAP POST with: ' + function_call)

# Basic view accepting a POST which will just print the function called

#class SoapHandlerView(generics.GenericAPIView):
    #template_name = 'openCheezAI/function_detail.html'

#   def get_serializer_class(self):
#       return None 
#
#   def post(self, request, format=None):
#       '''
#       Get the SOAP xml from the post body, convert to a function
#       call, and print the call for reference.
#       '''
#       soapString = request.body
#       function_call = soapStringToFunctionCall(soapString)
#       context['function_call'] = soapStringToFunctionCall(soapString)
#       #return HttpResponse(function_call)
#       return Response('you called SOAP POST')

#   def get(self, request, format=None):
#       return Response('you called SOAP GET, BABY!!')
#
#-------------------------------------------------------------------------------
# UTILITY FUNCTIONS
#-------------------------------------------------------------------------------

def soapStringToFunctionCall(soapString):

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

