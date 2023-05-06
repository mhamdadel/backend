from django.contrib import admin
from django.urls import include, path, re_path
from .views import all_base, base_detail, error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', all_base),
    path('api/base/<int:id>/', base_detail),
    path('api/auth/', include('authentication.urls')),
    path('api/ecommerce/', include('ecommerce.urls')),
    path('orders/', include('orders.urls')),
    path('paypal/',include('paypal.standard.ipn.urls')),
    path('payment/', include('payment.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),

    # re_path(r'^.*$', error_404),
]