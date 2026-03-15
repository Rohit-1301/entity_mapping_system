from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

class ProductCourseMappingListCreateAPIView(APIView):
    """
    API View to list all product-course mappings and create a new mapping.
    """
    def get(self, request):
        product_id = request.query_params.get('product_id')
        course_id = request.query_params.get('course_id')
        mappings = ProductCourseMapping.objects.all()

        if product_id:
            mappings = mappings.filter(product_id=product_id)
        if course_id:
            mappings = mappings.filter(course_id=course_id)

        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a product-course mapping.
    """
    def get_object(self, id):
        try:
            return ProductCourseMapping.objects.get(id=id)
        except ProductCourseMapping.DoesNotExist:
            return None

    def get(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        mapping.delete()
        return Response({"message": "Mapping deleted successfully"}, status=status.HTTP_200_OK)

