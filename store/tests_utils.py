from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate

from store.models import Product


User = get_user_model()


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Title",
            description="Description",
            height=1,
            width=2,
            length=3,
            material="Material",
            price=123,
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
        self.user.favourite.toggle(self.product)

        # def test_toggle_cart(self):
        #     cart.toggle(self.user.cart, self.product)
        #     cart.toggle(self.user.cart, self.product)

        # def test_rate(self):
        #     rating = 2
        #     self.product.rate(rating)
        #     self.product.get_rating()
