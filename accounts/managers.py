from django.contrib.auth.base_user import BaseUserManager
from store.models import Favourite, Cart


# Create your managers here
class AccountManager(BaseUserManager):
    """
    Custom user model manager with ability to create users with custom 
    attributes and permissions.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create user with unique favourite and cart
        """
        user = super().create_user(self, username, email, password, **extra_fields)
        user_fav = Favourite()
        user_cart = Cart()
        user_fav.save()
        user_cart.save()
        user.cart = user_cart
        user.favourite = user_fav
        user.save()
        return user
