from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from store.models import Favourite, Cart
from .managers import AccountManager


# Create your models here.
class Account(AbstractBaseUser):
    favourite = models.OneToOneField(
        Favourite,
        verbose_name=("Favourite products"),
        on_delete=models.CASCADE,
        unique=True
    )
    cart = models.OneToOneField(
        Cart,
        verbose_name=("Products in cart"),
        on_delete=models.CASCADE,
        unique=True
    )

    objects = AccountManager
