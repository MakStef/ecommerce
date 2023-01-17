from django.test import TestCase

from .utils.utils import (
    User, 
    get_random_categories,
    get_last_products,
    products_to_values_list,
)

from .models import Product, Subcategory, Category, Supercategory
from api.tests import create_products, create_supercats, create_cats, create_subcats

class UtilsTestCase(TestCase):
    def setUp(self):
        create_supercats()
        create_cats()
        create_subcats()
        create_products()

        User.objects.create(username='bob', email='bob@example.com', password='set123ASD')

    def test_get_rand_cats(self):
        get_random_categories(6)

    def test_get_last_prods(self):
        get_last_products(cats=Category.objects.all()[:2])

    def test_products_to_values_list(self):
        products_to_values_list(products=Product.objects.all()[:8])