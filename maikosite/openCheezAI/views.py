from django.shortcuts import render

from openCheezAI.models import Person
from openCheezAI.serializers import PersonSerializer

from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

# Create your views here.

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
        'persons': reverse('openCheezAI:person-list', request=request, format=format),
    })
