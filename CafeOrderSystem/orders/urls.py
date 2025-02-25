from rest_framework.routers import DefaultRouter
from .views import MealViewSet, OrderViewSet


app_name = 'orders'
router = DefaultRouter()
router.register('meal', MealViewSet, basename='meal')
router.register('order', OrderViewSet, basename='order')

urlpatterns = router.urls