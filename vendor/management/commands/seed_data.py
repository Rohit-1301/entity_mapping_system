from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

class Command(BaseCommand):
    help = 'Seeds the database with predefined data for all modules'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Vendors
        v1, _ = Vendor.objects.get_or_create(name='Amazon Web Services', code='AWS', description='Cloud Service Provider')
        v2, _ = Vendor.objects.get_or_create(name='Microsoft', code='MSFT', description='Software and Cloud Provider')
        v3, _ = Vendor.objects.get_or_create(name='Google Cloud', code='GCP', description='Cloud Computing Services')

        # 2. Create Products
        p1, _ = Product.objects.get_or_create(name='AWS Managed Services', code='AWS-MS', description='Managed services for AWS')
        p2, _ = Product.objects.get_or_create(name='Azure Cloud Services', code='AZ-CS', description='Microsoft Azure cloud suite')
        p3, _ = Product.objects.get_or_create(name='Google Engine', code='GCP-E', description='Compute engine for GCP')

        # 3. Create Courses
        c1, _ = Course.objects.get_or_create(name='AWS Solutions Architect', code='AWS-SA', description='Learn AWS architecture')
        c2, _ = Course.objects.get_or_create(name='Azure Fundamentals', code='AZ-900', description='Basics of Microsoft Azure')
        c3, _ = Course.objects.get_or_create(name='GCP Cloud Digital Leader', code='GCP-DL', description='Cloud business basics')

        # 4. Create Certifications
        cert1, _ = Certification.objects.get_or_create(name='AWS Certified Solutions Architect Associate', code='AWS-SAA', description='Associate level AWS cert')
        cert2, _ = Certification.objects.get_or_create(name='Microsoft Certified: Azure Fundamentals', code='MS-AZ-900', description='Entry level Azure cert')
        cert3, _ = Certification.objects.get_or_create(name='Google Cloud Digital Leader', code='GCP-CDL', description='Business professional cert')

        # 5. Create Mappings
        # Vendor -> Product
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p1, primary_mapping=True)
        VendorProductMapping.objects.get_or_create(vendor=v2, product=p2, primary_mapping=True)
        VendorProductMapping.objects.get_or_create(vendor=v3, product=p3, primary_mapping=True)

        # Product -> Course
        ProductCourseMapping.objects.get_or_create(product=p1, course=c1, primary_mapping=True)
        ProductCourseMapping.objects.get_or_create(product=p2, course=c2, primary_mapping=True)
        ProductCourseMapping.objects.get_or_create(product=p3, course=c3, primary_mapping=True)

        # Course -> Certification
        CourseCertificationMapping.objects.get_or_create(course=c1, certification=cert1, primary_mapping=True)
        CourseCertificationMapping.objects.get_or_create(course=c2, certification=cert2, primary_mapping=True)
        CourseCertificationMapping.objects.get_or_create(course=c3, certification=cert3, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
