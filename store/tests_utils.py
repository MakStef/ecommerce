from django.test import TestCase

from .utils.utils import (
    User, 
    get_random_categories,
    get_last_products,
    products_to_values_list,
)

from .models import Product, Subcategory, Category, Supercategory


class UtilsTestCase(TestCase):
    def setUp(self):
        def create_supercats():
            for num in range(1, 5):
                Supercategory.objects.create(title=f"sup{num}")

        def create_cats():
            for sup in Supercategory.objects.all():
                for num in range(1, 5):
                    Category.objects.create(title=f"{sup.title}cat{num}", supercat=sup)

        def create_subcats():
            for cat in Category.objects.all():
                for num in range(1, 5):
                    Subcategory.objects.create(title=f"{cat.title}sub{num}", cat=cat)
            
        def create_products():
            for sub in Subcategory.objects.all():
                for num in range(1, 5):
                    Product.objects.create(
                        title=f"{sub.title}product{num}",
                        description='Example',
                        height='1',
                        width='2',
                        length='3',
                        material='Nothing',
                        price=123,
                        discount=0,
                        subcat=sub,
                    )
        
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