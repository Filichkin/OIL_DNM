from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.users.views import (
    DealerViewSet,
    SupplierViewSet,
    UserViewSet
)
from api.orders.views import OrderViewSet
from api.catalog.views import (
    CatalogViewSet,
    CartView,
    ProductViewSet
)


app_name = 'api'

router = DefaultRouter()

router.register('catalog', CatalogViewSet, 'catalog')
router.register('dealers', DealerViewSet, 'dealers')
router.register('orders', OrderViewSet, 'orders')
router.register('products', ProductViewSet, 'products')
router.register('suppliers', SupplierViewSet, 'suppliers')
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('cart/', CartView.as_view(), name='cart_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
