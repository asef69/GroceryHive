
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from catalog.views import CategoryViewSet, ProductViewSet
from reviews.views import ReviewViewSet
from orders.views import CartItemViewSet, CheckoutView, PurchaseHistoryView, SellerDashboardView, OrderItemViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


schema_view = get_schema_view(
    openapi.Info(
        title="Grocery Shop API",
        default_version="v1",
        description="API docs for Grocery Shop",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


root = routers.SimpleRouter() # type: ignore
root.register(r"api/catalog/categories", CategoryViewSet, basename="category")
root.register(r"api/catalog/products", ProductViewSet, basename="product")
root.register(r"api/orders/cart", CartItemViewSet, basename="cart")


cat_products = routers.NestedSimpleRouter(root, r"api/catalog/categories", lookup="category")
cat_products.register(r"products", ProductViewSet, basename="category-products")


prod_reviews = routers.NestedSimpleRouter(root, r"api/catalog/products", lookup="product")
prod_reviews.register(r"reviews", ReviewViewSet, basename="product-reviews")


from orders.views import OrderViewSet
root.register(r"api/orders/orders", OrderViewSet, basename="order")
order_items = routers.NestedSimpleRouter(root, r"api/orders/orders", lookup="order")
order_items.register(r"items", OrderItemViewSet, basename="order-items")

urlpatterns = [
    path("admin/", admin.site.urls),

    
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),

    
    path("api/users/", include("users.urls")),
    path("api/wallet/", include("wallet.urls")),
    

    
    *root.urls,
    *cat_products.urls,
    *prod_reviews.urls,
    *order_items.urls,

    
    path("api/orders/checkout/", CheckoutView.as_view(), name="checkout"),
    path("api/orders/history/", PurchaseHistoryView.as_view(), name="purchase-history"),
    path("api/orders/seller/dashboard/", SellerDashboardView.as_view(), name="seller-dashboard"),

    
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('djoser.urls')),  
    path('auth/', include('djoser.urls.jwt')),  
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)