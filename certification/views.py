from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certification
from .serializers import CertificationSerializer

class CertificationListCreateAPIView(APIView):
    """
    API View to list all certifications and create a new certification.
    """
    def get(self, request):
        active_status = request.query_params.get('is_active')
        certifications = Certification.objects.all()
        
        if active_status is not None:
            is_active = active_status.lower() == 'true'
            certifications = certifications.filter(is_active=is_active)
            
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a certification instance.
    """
    def get_object(self, id):
        try:
            return Certification.objects.get(id=id)
        except Certification.DoesNotExist:
            return None

    def get(self, request, id):
        certification = self.get_object(id)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        certification = self.get_object(id)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        certification = self.get_object(id)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        certification = self.get_object(id)
        if not certification:
            return Response({"error": "Certification not found"}, status=status.HTTP_404_NOT_FOUND)
        certification.delete()
        return Response({"message": "Certification deleted successfully"}, status=status.HTTP_200_OK)
