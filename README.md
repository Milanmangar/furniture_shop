# Furniture Factory
test project for global logic

**How to get started normal way**
1) clone the project using https://github.com/Milanmangar/global_logic_furniture_company.git in command prompt
2) cd furniture_factory/django-furniture_factory/furniture_factory
3) pip install -r requirements.txt (can be ran directly or create virtual environment and run it inside virtual environment)
4) create folder table_data/logs in path furniture_factory/django-furniture_factory/furniture_factory ``skip it, if folder alreay present``
5) python manage.py migrate
6) python manage.py createsuperuser and fill in the details
7) python manage.py runserver, this will run django project in http://127.0.0.0:8000
8) go to URL http://127.0.0.0:8000/admin, login to admin panel using superuser credentials
9) add data to ``Feet`` table and then add data to ``Leg`` table and then add data to ``Table`` table
10) test the api in postman


**Api details**

1) API can be seen with the help swagger url in http://localhost:8000/swagger/, login with the super user credentials
2) or import, exported postman file in path ``furniture_factory\django-furniture_factory\furniture_factory\furniture_factory_api_details.postman_collection.json``

**How to get started with pip install package  name**
1) cd furniture_factory/django-furniture_factory/
2) follow instruction in README.rst file

**Functionality included**

***Table Module***

1) Methods included: GET, POST, PUT, PATCH, DELETE, GET(to retrieve particular data)
2) Authentication(TokenAuthentication)
3) Custom Authentication class, which will only require authentication for POST, PUT, PATCH, DELETE, for GET
   no authentication is needed
4) Test cases covered for all methods(GET, POST, PUT, PATCH, DELETE, GET(to retrieve particular data)) and also for authentication check
5) Logging
6) Exception handling
7) Django Swagger included
8) pip install the project as package

***Functionality included due to time contraint***

1) Legs 
2) Feet