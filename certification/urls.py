from django.urls import path
from .views import CertificationListCreateAPIView, CertificationDetailAPIView

urlpatterns = [
    path('certifications/', CertificationListCreateAPIView.as_view(), name='certification-list-create'),
    path('certifications/<int:id>/', CertificationDetailAPIView.as_view(), name='certification-detail'),
]
