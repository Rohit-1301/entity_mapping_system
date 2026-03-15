from django.db import models
from product.models import Product
from course.models import Course

class ProductCourseMapping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='course_mappings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='product_mappings')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'course') # Prevents duplicate product-course pairs
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} -> {self.course.name}"

