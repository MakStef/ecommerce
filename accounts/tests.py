from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


# Create your tests here.
class AccountTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )
        user.save()

    def test_login_user(self):
        User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        ).save()

        user = self.client.login(
            username="testuser",
            password="testpassword123",
        )

        if not user:
            raise LookupError(f'{User} not found')
