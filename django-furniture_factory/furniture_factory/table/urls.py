from table.table_api.api import TableViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TableViewset, basename='table_viewset')
app_name = 'table'
urlpatterns = router.urls
