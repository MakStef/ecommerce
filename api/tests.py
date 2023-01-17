from django.test import TestCase, Client
from store.models import Product, Subcategory, Category, Supercategory
from store.utils import utils
from random import randint

import json


def create_supercats(k: int=5):
    for num in range(1, k):
        Supercategory.objects.create(title=f"sup{num}")

def create_cats(k: int=5):
    for sup in Supercategory.objects.all():
        for num in range(1, k):
            Category.objects.create(title=f"{sup.title}cat{num}", supercat=sup)

def create_subcats(k: int=5):
    for cat in Category.objects.all():
        for num in range(1, k):
            Subcategory.objects.create(title=f"{cat.title}sub{num}", cat=cat)
    
def create_products(k: int=5):
    for sub in Subcategory.objects.all():
        for num in range(1, k):
            Product.objects.create(
                title=f"{sub.title}product{num}",
                description='Example',
                height='1',
                width='2',
                length='3',
                material='Nothing',
                price=randint(120, 450),
                discount=randint(0, 1),
                subcat=sub,
            )


class DefaultAPITestCase(TestCase):
    def setUp(self):
        create_supercats()
        create_cats()
        create_subcats()
        create_products()


class TestProductsApi(DefaultAPITestCase):
    def test_get_products_by_subcategory(self):
        c = Client()
        sub_id = Subcategory.objects.all().order_by('created_at')[0].id
        subprods = c.get(f'/api/products?subcategory_id={sub_id}', follow=True)
        
        response_correct = subprods.status_code == 200

        expected_response = utils.products_to_values_list(Product.objects.filter(subcat=sub_id))
        actual_response = json.loads(subprods.content)
        products_correct = expected_response == actual_response

        self.assertTrue(response_correct, 'Wrong code: %s' % subprods.status_code)
        self.assertTrue(products_correct, f'\n\nWRONG PRODUCTS:\n\nexpected: {expected_response}\n\nrecieved: {actual_response}')

    def test_get_products_by_cat(self):
        c = Client()
        cat_id = Category.objects.all()[0].id
        catprods = c.post(f'/products?category_id={cat_id}')
        self.assertTrue(catprods.status_code == 200)

    def test_get_products_by_supercat(self):    
        c = Client()
        sup_id = Supercategory.objects.all()[0].id
        supprods = c.post(f'/products?supercategory_id={sup_id}')
        supprods.status_code == 200
        self.assertTrue(supprods.status_code == 200)

    def test_get_products_with_count(self):
        c = Client()
        prods = c.post(f'/products?count=4')
        self.assertEqual(len(json.loads(prods.content)), 4)

    def test_get_products_with_ordering(self):
        c = Client()
        prods = c.post(f'/products?ordering=discounted')
        prod_id = json.loads(prods.content)[0].id
        awaited_id = Product.objects.all().order_by('discounted')[0].id
        self.assertTrue(prod_id == awaited_id)

    def test_get_products_with_price_span(self):
        c = Client()
        prods = c.post(f'/products?price_span=200_300')
        to_compare = Product.objects.filter(price__lte=300, price__gte=200)[0]
        expr = to_compare.id == json.loads(prods.content)[0].id
        self.assertTrue(expr)



class TestSubcategoryApi(DefaultAPITestCase):
    pass


class TestCategoryApi(DefaultAPITestCase):
    pass


class TestSupercategoryApi(DefaultAPITestCase):
    pass
