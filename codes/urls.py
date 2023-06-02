from rest_framework.routers import DefaultRouter

from codes import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('codes', views.CodeViewSet, basename='codes')
urlpatterns = router.urls
