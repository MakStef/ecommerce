from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product(
            title="Title",
            description="Description",
            height=1,
            width=2,
            length=3,
            material="Material",
            price=123,
        )
        User.objects.create_user(
            self,
            username="Testuser",
            email="test@gmail.com",
            password="testpassword123"
        )

    def add_favourite(self):
        self.user.favourite.products.add(self.product)
        print(self.product.title)

    def add_cart(self):
        self.user.cart.products.add(self.product)
