from django.urls import path
from .views import (
    HomepageView,
    FilterView,
    SearchView,
    ProductView,
    NewslettersView,
)
app_name = 'store'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('filter/<slug:cat_slug>', FilterView.as_view(), name='filter'),
    path('search/<str:wanted>', SearchView.as_view(), name='search'),
    path('product/<slug:product_slug>', SearchView.as_view(), name='search'),
    path('newsletters/', NewslettersView.as_view(), name='newsletter'),
]
