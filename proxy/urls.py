from django.conf.urls import url, include

from data_office.urls import urlpatterns

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include((urlpatterns, 'data_office'), namespace='data_office')),
]
