# Entity Mapping System - Django REST Framework Assignment

A modular Django backend system for managing Master Entities (Vendors, Products, Courses, Certifications) and their Mappings. Built strictly using **APIView** and following a highly modular architecture.

## Table of Contents
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Seed Data](#database-seed-data)
- [Validation Rules](#validation-rules)
- [Filtering](#filtering)

---

## Architecture

The project is divided into several independent Django apps to ensure modularity:

### Master Apps
- **vendor**: Manages Vendor master data.
- **product**: Manages Product master data.
- **course**: Manages Course master data.
- **certification**: Manages Certification master data.

### Mapping Apps
- **vendor_product_mapping**: Bridges Vendors and Products.
- **product_course_mapping**: Bridges Products and Courses.
- **course_certification_mapping**: Bridges Courses and Certifications.

---

## Technologies
- **Python 3.x**
- **Django 5.x**
- **Django REST Framework**
- **drf-yasg** (Swagger/ReDoc)

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd entity_mapping_system
```

### 2. Set up a virtual environment (Optional but Recommended)
```bash
# Using Conda
conda create -n entity_system_env python=3.10
conda activate entity_system_env

# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django djangorestframework drf-yasg
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Running the Application

Start the development server:
```bash
python manage.py runserver
```
The app will be available at `http://127.0.0.1:8000/`.

### Create a Superuser (for Admin Access)
```bash
python manage.py createsuperuser
```
Access the Django Admin at `http://127.0.0.1:8000/admin/`.

---

## API Documentation

The project uses `drf-yasg` for automatic API documentation.

- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

Each API has been documented with relevant query parameters and response schemas.

---

## Database Seed Data

A management command is included to prepopulate the database with sample data:
```bash
python manage.py seed_data
```
This will create:
- 3 Vendors (AWS, Microsoft, GCP)
- 3 Products
- 3 Courses
- 3 Certifications
- Primary mappings connecting them all.

---

## Validation Rules

1. **Unique Code**: Every master entity must have a unique `code`.
2. **Duplicate Mapping Prevention**: The system prevents creating the same mapping (e.g., Vendor A -> Product B) twice.
3. **One Primary Mapping**: For any master entity, only one child mapping can be marked as `primary_mapping=True`.
   - *Example*: A Vendor can have multiple Products, but only one can be the "Primary Product".
4. **Required Fields**: Standard DRF validation ensures all mandatory fields are present.

---

## Filtering

List APIs support filtering via query parameters:

- **Master List Filtering**:
  - `GET /api/products/?vendor_id=1`
  - `GET /api/courses/?product_id=2`
  - `GET /api/certifications/?course_id=3`
- **Mapping List Filtering**:
  - `GET /api/vendor-product-mappings/?vendor_id=1`
  - `GET /api/product-course-mappings/?product_id=2`

All list APIs also support `is_active=true/false` filtering.

---

## Implementation Details

- **APIView Only**: Every endpoint is a subclass of `rest_framework.views.APIView`. No `ViewSets` or `GenericAPIViews` were used.
- **Manual CRUD**: Each view manually implements `get`, `post`, `put`, `patch`, and `delete` methods.
- **Manual Object Fetching**: Uses a private `get_object` helper with `try/except` for handling `DoesNotExist`.
- **Modularity**: Each app contains its own `models.py`, `serializers.py`, `views.py`, `urls.py`, and `admin.py`.
