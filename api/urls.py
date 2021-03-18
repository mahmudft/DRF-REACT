from rest_framework import urlpatterns
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', views.ProductListView)
#router.register('addtocart', views.handle_cart)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('addcart/', views.add_item),
    path('orders/', views.order_list),
    path('checkout/', views.checkout),
    path('deleteorder/', views.removefromcard),
]