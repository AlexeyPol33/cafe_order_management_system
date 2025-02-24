from rest_framework.routers import DefaultRouter
from .views import MealViewSet


app_name = 'orders'
router = DefaultRouter()
router.register('meal', MealViewSet,basename='meal')

urlpatterns = router.urls