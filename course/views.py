from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CourseListCreateAPIView(APIView):
    """
    API View to list all courses and create a new course.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        active_status = request.query_params.get('is_active')
        product_id = request.query_params.get('product_id')
        courses = Course.objects.all()
        
        if active_status is not None:
            is_active = active_status.lower() == 'true'
            courses = courses.filter(is_active=is_active)
        
        if product_id:
            courses = courses.filter(product_mappings__product_id=product_id)
            
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a course instance.
    """
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            return None

    def get(self, request, id):
        course = self.get_object(id)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        course = self.get_object(id)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        course = self.get_object(id)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        course = self.get_object(id)
        if not course:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=status.HTTP_200_OK)
