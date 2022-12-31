from django.views.generic import View
from django.core.serializers import serialize
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

from store.models import Product, Category, Supercategory, Subcategory
from store.utils.utils import products_to_values_list

import json


def get_products(request):
    queryset = Product.objects.all()

    if request.GET.get('subcategory_id'):
        queryset = queryset.filter(subcat_id=request.GET.get('subcategory_id'))
    elif request.GET.get('category_id'):
        queryset = queryset.filter(cat_id=request.GET.get('category_id'))
    elif request.GET.get('supercategory_id'):
        queryset = queryset.filter(supercat_id=request.GET.get('supercategory_id'))
    
    if request.GET.get('ordering'):
        queryset = queryset.order_by(request.GET.get('ordering'))
    
    if request.GET.get('count'):
        lim = int(request.GET.get('count'))
        queryset = queryset[:lim]

    data = products_to_values_list(queryset, request.user if request.user is not AnonymousUser else None)
    return JsonResponse(json.dumps(data), safe=False)

def get_subcats(request):
    queryset = Subcategory.objects.all()
    
    if request.GET.get('category_id'):
        queryset = queryset.filter(cat_id=request.GET.get('category_id'))
    elif request.GET.get('supercategory_id'):
        queryset = queryset.filter(cat__supercat_id=request.GET.get('supercategory_id'))
    
    if request.GET.get('ordering'):
        queryset = queryset.order_by(request.GET.get('ordering'))

    data = list(queryset.values_list('title', 'slug', 'created_at'))

    return JsonResponse(data, safe=False)

def get_cats(request):
    queryset = Category.objects.all()

    if request.GET.get('supercategory_id'):
        queryset = queryset.filter(supercat_id=request.GET.get('supercategory_id'))

    if request.GET.get('ordering'):
        queryset = queryset.order_by(request.GET.get('ordering'))

    data = list(Category.objects.all().values_list('title', 'slug', 'created_at'))

    return JsonResponse(data, safe=False)

def get_supcats(request):
    queryset = Supercategory.objects.all().values_list('title', 'slug', 'created_at')

    if request.GET.get('ordering'):
        queryset = queryset.order_by(request.GET.get('ordering'))

    data = list(queryset)
    return JsonResponse(data, safe=False)