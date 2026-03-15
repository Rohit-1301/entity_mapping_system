from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 
            'product', 
            'course', 
            'primary_mapping', 
            'is_active', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        product = data.get('product')
        course = data.get('course')
        primary_mapping = data.get('primary_mapping', False)

        # Check for duplicate mapping (creation only)
        if not self.instance:
            if ProductCourseMapping.objects.filter(product=product, course=course).exists():
                raise serializers.ValidationError({
                    "non_field_errors": "This product-course mapping already exists."
                })

        # Check for only one primary mapping per product
        if primary_mapping:
            queryset = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": f"Product '{product.name}' already has a primary course mapping."
                })

        return data
