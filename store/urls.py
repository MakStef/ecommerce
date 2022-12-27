from django.urls import path
from .views import (
    HomepageView,
    SearchView,
    ProductView,
    ProductsView,
    NewslettersView,
)
app_name = 'store'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('search/<str:wanted>', SearchView.as_view(), name='search'),
    path('products/', ProductsView.as_view(), name='products'),
    path('product/<slug:product_slug>', SearchView.as_view(), name='product'),
    path('newsletters/', NewslettersView.as_view(), name='newsletter'),
]
