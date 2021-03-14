from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from table import urls as table_urls

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path(r'swagger/', schema_view),
    path('api/table/', include(table_urls, namespace='table_api')),
]
