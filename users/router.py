from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'patients', views.PatientViewSet)
#router.register(r'data_sets', views.DataSetViewSet)
