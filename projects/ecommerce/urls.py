
from django.urls import path
from . import views

urlpatterns = [
    path('product', views.ProductViewSet.as_view({'get': 'list'}), name="product"),
]