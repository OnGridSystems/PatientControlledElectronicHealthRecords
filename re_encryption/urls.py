from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from users.urls import urlpatterns
from re_encryption import views

urlpatterns = [
    url(r'^records/$', views.RecordsSetList.as_view(), name='records-sets-list'),
    url(r'^records/edit/(?P<pk>[0-9]+)/$', views.RecordsSetRecepientUpdate.as_view(), name='records-set-detail'),
    url(r'^records/(?P<pk>[0-9]+)/$', views.RecordsSetRecepientDetail.as_view(), name='records-set-detail'),
    url(r'^records/add/$', views.RecordsSetCreation.as_view(), name='records-sets-add'),
    url(r'^me/records/$', views.RecordsSetOwnList.as_view(), name='records-sets-own-list'),
]
