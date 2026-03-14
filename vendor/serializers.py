from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id', 
            'name', 
            'code', 
            'description', 
            'is_active', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """
        Check that the vendor code is unique.
        """
        # Unique validation is already handled by ModelSerializer because of unique=True in the model,
        # but we can add custom logic here if needed.
        return value
