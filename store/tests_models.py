from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from api.tests import create_products, create_supercats, create_cats, create_subcats
from store.models import (
    Product,
    Subcategory,
    Category,
    Supercategory,
    Favourite,
    Cart,
)


User = get_user_model()


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        supercat = Supercategory.objects.create(title='sup1')
        supercat.save()
        cat = Category.objects.create(title='cat1', supercat=supercat)
        cat.save()
        subcat = Subcategory.objects.create(title='sub1', cat=cat)
        subcat.save()
        self.product = Product.objects.create(
            title="Title",
            description="Description",
            height=1,
            width=2,
            length=3,
            material="Material",
            price=123,
            discount=0,
            subcat=subcat,
        )
        self.user = User.objects.create_user(
            username="Testuser",
            email="test@gmail.com",
            password="testpassword123"
        )
        self.product.save()
        self.user.save()

    def test_toggle_favourite(self):
        self.user.favourite.toggle(self.product)
        print(self.user.favourite.products.all())
        self.user.favourite.toggle(self.product)
        print(self.user.favourite.products.all())

    def test_toggle_cart(self):
        self.user.cart.toggle(self.product)
        self.user.cart.toggle(self.product)

    def test_rating(self):
        rating = 2
        self.product.rate(rating, self.user)
        self.product.get_rating()


class CategoriesTestCase(TestCase):
    def setUp(self):
        create_supercats()
        create_cats()
        create_subcats()
        create_products()

    def test_get_supercat_products(self):
        all_products = []
        for sup in Supercategory.objects.all():
            all_products.extend(list(sup.get_products()))
        if len(all_products) != Product.objects.all().count():
            raise AssertionError('SUPERCATS get_products() FAILURE', len(all_products), Supercategory.objects.all().count())

    def test_get_cat_products(self):
        all_products = []
        for cat in Category.objects.all():
            all_products.extend(list(cat.get_products()))
        if len(all_products) != Product.objects.all().count():
            raise AssertionError('CATS get_products() FAILURE', len(all_products), Product.objects.all().count())

    def test_get_subcat_products(self):
        all_products = []
        for subcat in Subcategory.objects.all():
            all_products.extend(list(subcat.get_products()))
        if len(all_products) != Product.objects.all().count():
            raise AssertionError('SUBCATS get_products() FAILURE', len(all_products), Subcategory.objects.all().count())

    def test_get_supercat_cats(self):
        all_cats=[]
        for supercat in Supercategory.objects.all():
            all_cats.extend(list(supercat.get_cats()))
        if len(all_cats) != Category.objects.all().count():
            raise AssertionError('SUPERCATS get_cats() FAILURE')

    def test_get_cat_subcats(self):
        all_subcats=[]
        for cat in Category.objects.all():
            all_subcats.extend(list(cat.get_subcats()))
        if len(all_subcats) != Subcategory.objects.all().count():
            raise AssertionError('CATS get_subcats() FAILURE')