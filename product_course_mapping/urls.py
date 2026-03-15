from django.urls import path
from .views import ProductCourseMappingListCreateAPIView, ProductCourseMappingDetailAPIView

urlpatterns = [
    path('product-course-mappings/', ProductCourseMappingListCreateAPIView.as_view(), name='product-course-mapping-list-create'),
    path('product-course-mappings/<int:id>/', ProductCourseMappingDetailAPIView.as_view(), name='product-course-mapping-detail'),
]
