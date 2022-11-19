from django.test import TestCase
from django.contrib.auth import get_user_model
from store.models import Product


User = get_user_model()


# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            self,
            username="Testuser",
            email="test@gmail.com",
            password="testpassword123"
        )
