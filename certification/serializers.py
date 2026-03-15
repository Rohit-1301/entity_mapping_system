from rest_framework import serializers
from .models import Certification

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
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
        Check that the certification code is unique.
        """
        # Unique validation is already handled by ModelSerializer because of unique=True in the model.
        return value
