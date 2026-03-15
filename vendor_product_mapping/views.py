from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

class VendorProductMappingListCreateAPIView(APIView):
    """
    API View to list all vendor-product mappings and create a new mapping.
    """
    def get(self, request):
        vendor_id = request.query_params.get('vendor_id')
        product_id = request.query_params.get('product_id')
        mappings = VendorProductMapping.objects.all()

        if vendor_id:
            mappings = mappings.filter(vendor_id=vendor_id)
        if product_id:
            mappings = mappings.filter(product_id=product_id)

        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):
    """
    API View to retrieve, update, and delete a vendor-product mapping.
    """
    def get_object(self, id):
        try:
            return VendorProductMapping.objects.get(id=id)
        except VendorProductMapping.DoesNotExist:
            return None

    def get(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        mapping = self.get_object(id)
        if not mapping:
            return Response({"error": "Mapping not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
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

