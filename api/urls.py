from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BiomaterialViewSet, MedicalFilesViewSet, MedicalReportsViewSet,
    MedicalTestsViewSet, PatientsViewSet, TestSamplesViewSet
)

router = DefaultRouter()
router.register(r'biomaterials', BiomaterialViewSet, basename='biomaterial')
router.register(r'medical-files', MedicalFilesViewSet, basename='medical-files')
router.register(r'medical-reports', MedicalReportsViewSet, basename='medical-reports')
router.register(r'medical-tests', MedicalTestsViewSet, basename='medical-tests')
router.register(r'patients', PatientsViewSet, basename='patients')
router.register(r'test-samples', TestSamplesViewSet, basename='test-samples')

urlpatterns = [
    path('', include(router.urls)),
]
