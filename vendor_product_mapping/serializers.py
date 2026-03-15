from rest_framework import serializers
from .models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = [
            'id', 
            'vendor', 
            'product', 
            'primary_mapping', 
            'is_active', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        vendor = data.get('vendor')
        product = data.get('product')
        primary_mapping = data.get('primary_mapping', False)

        # Check for duplicate mapping (only on create)
        if not self.instance:
            if VendorProductMapping.objects.filter(vendor=vendor, product=product).exists():
                raise serializers.ValidationError({
                    "non_field_errors": "This vendor-product mapping already exists."
                })

        # Check for multiple primary mappings for the same vendor
        if primary_mapping:
            queryset = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if self.instance:
                # Exclude the current instance if updating
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": f"Vendor '{vendor.name}' already has a primary product mapping."
                })

        return data
