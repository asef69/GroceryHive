from django.urls import path
from .views import MyWalletView,DepositView

urlpatterns = [
    path('me/',MyWalletView.as_view(),name='my-wallet'),
    path('deposit/',DepositView.as_view(),name='deposit'),
]
