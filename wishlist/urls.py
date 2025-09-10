
from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet

router = DefaultRouter()
router.register("", WishlistViewSet, basename="wishlist")
urlpatterns = router.urls
