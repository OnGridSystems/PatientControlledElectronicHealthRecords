from django.conf.urls import url, include

from users.urls import urlpatterns

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include((urlpatterns, 'users'), namespace='users')),
]
