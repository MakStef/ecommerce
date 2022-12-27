from random import sample

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from store.models import (
    Product,
    Subcategory,
    Category,
    Supercategory,
)

User = get_user_model()

def get_random_categories(k: int):
    models = [Subcategory, Category, Supercategory] 
    cats = []
    map(lambda mdl: cats+list(mdl.objects.all()), models)
    return list (
        sample(population=cats, k=k) 
        if len(cats) > k 
        else sample(population=cats, k=len(cats))
    )

def get_last_products(cats: list, k:int=9):
    cats_products = {}
    for cat in cats:
        cats_products[f'{cat.title}'] = cat.get_products(ordering="created_at")[:k]

    return cats_products

def products_to_values_list(products: QuerySet, user:User=None):
    lst = []

    for product in products:
        lst.append({
            'id' : product.pk,
            'image' : product.image.url if product.image else 'https://www.guede-solingen.de/wp-content/uploads/2021/04/guede-theknife-jade--uai-1706x1280.jpg',
            'title' : product.title,
            'size' : f'{product.height}x{product.width}x{product.length}',
            'materials': product.material,
            'rating' : product.get_rating(),
            'personal_rating': product.votes.get(user_id=user_id).value if user and product.votes.filter(user_id=user.pk).exists() else None,
            'rate_count' : product.votes.all().count(),
            'price' : product.price if product.discount != 0 else product.price - (product.price * (product.discount / 100)),
        })

    return lst
