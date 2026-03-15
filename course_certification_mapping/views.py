from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

class CourseCertificationMappingListCreateAPIView(APIView):
    """
    API View to list all course-certification mappings and create a new mapping.
    """
    def get(self, request):
        course_id = request.query_params.get('course_id')
        certification_id = request.query_params.get('certification_id')
        mappings = CourseCertificationMapping.objects.all()

        if course_id:
            mappings = mappings.filter(course_id=course_id)
        if certification_id:
            mappings = mappings.filter(certification_id=certification_id)

        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a course-certification mapping.
    """
    def get_object(self, id):
        try:
            return CourseCertificationMapping.objects.get(id=id)
        except CourseCertificationMapping.DoesNotExist:
            return None

    def get(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
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

