from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from users import views


router = routers.SimpleRouter()

urlpatterns = [
    url(r'^patients/$', views.PatientList.as_view(), name='patients-list'),
    url(r'^patients/(?P<pk>[0-9]+)/$', views.PatientDetail.as_view(), name='patient-detail'),
    url(r'^patients/signup/$', views.PatientCreation.as_view(), name='patient-signup'),
    url(r'^recepients/$', views.RecepientList.as_view(), name='recepients-list'),
    url(r'^recepients/(?P<pk>[0-9]+)/$', views.RecepientDetail.as_view(), name='recepient-detail'),
    url(r'^recepients/signup/$', views.RecepientCreation.as_view(), name='recepient-signup')
]

urlpatterns += router.urls
