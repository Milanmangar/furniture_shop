==================
Furniture Factory
==================


Quick start
-----------
1. pip install furniture_factory\django-furniture_factory\dist\django-furniture_factory-0.1.tar.gz

2. pip install djangorestframework django-rest-swagger

3. Add "table" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'rest_framework.authtoken',
        'rest_framework_swagger',
        'table',
    ]

4. Include the table URLconf in your project urls.py like this::

    path('table/', include('table.urls')),

5. Run ``python manage.py migrate`` to create the table models.

6. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

7. Visit http://127.0.0.1:8000/table/ to participate in the table api.