from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from users.urls import urlpatterns
from re_encryption.urls import urlpatterns as re_url_patterns

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='My API title')),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include((urlpatterns, 'users'), namespace='users')),
    url(r'^', include((re_url_patterns, 're_encryption'), namespace='re_encryption')),
]
