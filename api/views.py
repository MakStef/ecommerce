from django.views.generic import View
from django.http import JsonResponse
from django.core.serializers import serialize

from store.models import Product, Category, Supercategory, Subcategory


def get_products(request):
    queryset = Product.objects.all()

    if request.GET.get('subcategory_id'):
        queryset = queryset.filter(subcat_id=request.GET.get('subcategory_id'))
    elif request.GET.get('category_id'):
        queryset = queryset.filter(cat_id=request.GET.get('subcategory_id'))
    elif request.GET.get('supercategory_id'):
        queryset = queryset.filter(supercat_id=request.GET.get('subcategory_id'))
    
    if request.GET.get('ordering'):
        queryset = queryset.order_by(request.GET.get('ordering'))

    data = list(queryset.values_list(
        'title',
        'description',
        'height',
        'width',
        'length',
        'material',
        'price',
        'discount',
        'slug',
    ))
    return JsonResponse(data, safe=False)

def get_subcats(request):
    queryset = Subcategory.objects.all()
    
    if request.GET.get('category_id'):
        queryset = queryset.filter(cat_id=request.GET.get('subcategory_id'))
    elif request.GET.get('supercategory_id'):
        queryset = queryset.filter(cat__supercat_id=request.GET.get('subcategory_id'))
    
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