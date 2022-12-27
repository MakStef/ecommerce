from django.urls import path

from .views import (
    get_products,
    get_subcats,
    get_cats,
    get_supcats,
)

appname = 'api'

urlpatterns = [
    path('products/', get_products, name='get_products'),
    path('subcategories/', get_subcats, name='get_subcats'),
    path('categories/', get_cats, name='get_cats'),
    path('supercategories/', get_supcats, name='get_supcats'),
]
