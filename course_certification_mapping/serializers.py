from rest_framework import serializers
from .models import CourseCertificationMapping

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id', 
            'course', 
            'certification', 
            'primary_mapping', 
            'is_active', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        course = data.get('course')
        certification = data.get('certification')
        primary_mapping = data.get('primary_mapping', False)

        # 1. Prevent Duplicate Mapping (on creation only)
        if not self.instance:
            if CourseCertificationMapping.objects.filter(course=course, certification=certification).exists():
                raise serializers.ValidationError({
                    "non_field_errors": "This course-certification mapping already exists."
                })

        # 2. Only One Primary Mapping Per Course
        if primary_mapping:
            queryset = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                # Exclude the current mapping if we're updating it
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    "primary_mapping": f"Course '{course.name}' already has a primary certification mapping."
                })

        return data
