from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from data_office import views
 
urlpatterns = [
    url(r'^records/$', views.RecordsSetList.as_view(), name='records-sets-list'),
    url(r'^records/(?P<pk>[0-9]+)/$', views.RecordsSetDetail.as_view(), name='records-set-detail'),
    url(r'^patients/$', views.PatientList.as_view(), name='patients-list'),
    url(r'^patients/(?P<pk>[0-9]+)/$', views.PatientDetail.as_view(), name='patient-detail'),
    url(r'^signup/$', views.PatientCreation.as_view(), name='signup')
]
