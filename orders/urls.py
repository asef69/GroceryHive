# apps/orders/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CheckoutView, PurchaseHistoryView, SellerDashboardView

router = DefaultRouter()
router.register("cart", CartItemViewSet, basename="cart")

urlpatterns = [
    *router.urls,
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("history/", PurchaseHistoryView.as_view(), name="purchase-history"),
    path("seller/dashboard/", SellerDashboardView.as_view(), name="seller-dashboard"),
]
