from rest_framework import serializers
from openCheezAI.models import Person

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        url = serializers.HyperlinkedIdentityField(
            view_name = 'person-detail',
            lookup_field = 'uin'
        )
        fields = ( 'uin', 
                   'url',
                   'uiuc_netid', 
                   'uic_netid', 
                   'uis_netid', 
                   'illinois_netid', 
                   'uillinois_netid', 
                   'i2s_firstname', 
                   'i2s_lastname', 
                   'banner_firstname', 
                   'banner_lastname', 
                   'banner_suppressed',
                  )

