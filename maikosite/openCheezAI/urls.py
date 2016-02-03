from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from openCheezAI import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^persons/$',
        views.PersonList.as_view(),
        name='person-list'),
    url(r'^persons/(?P<pk>[0-9]+)$',
        views.PersonDetail.as_view(),
        name='person-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns.append(
    url(r'^soap/$',
        views.SoapHandlerView.as_view(),
        name='soap-handler-2'),
)
