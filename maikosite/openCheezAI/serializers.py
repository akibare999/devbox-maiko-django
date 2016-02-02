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
                   'illinois_netid', 
                   'uillinois_netid', 
                   'uic_netid', 
                   'uis_netid', 
                   'i2s_firstname', 
                   'i2s_lastname', 
                   'banner_firstname', 
                   'banner_lastname', 
                   'banner_suppressed',
                  )
        extra_kwargs = {
            'uin' : {'label': 'UIN'},
            'uiuc_netid' : {'label': 'UIUC NetID'},
            'illinois_netid' : {'label': 'Illinois NetID'},
            'uillinois_netid' : {'label': 'Enterprise NetID'},
            'uic_netid' : {'label': 'UIC NetID'},
            'uis_netid' : {'label': 'UIS NetID'},

            'banner_firstname' : {'label': 'Banner first name'},
            'banner_lastname' : {'label': 'Banner last name'},
            'i2s_firstname' : {'label': 'I2S first name'},
            'i2s_lastname' : {'label': 'I2S last name'},
            'banner_suppressed' : {'label': 'FERPA suppressed?'},
        }

