from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        editable=False
    )
    value = models.IntegerField(
        editable=False,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )


class Product(models.Model):
    title = models.CharField(verbose_name="Product title", max_length=255)
    image = models.ImageField(verbose_name="Product image")
    description = models.TextField(verbose_name="Product description")
    height = models.IntegerField(verbose_name="Product height")
    width = models.IntegerField(verbose_name="Product width")
    length = models.IntegerField(verbose_name="Product length")
    material = models.CharField(
        verbose_name="Product material",
        max_length=255
    )
    price = models.IntegerField(verbose_name="Product price")

    rating = models.IntegerField(
        default=0,
        editable=False,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    votes = models.ManyToManyField('Vote')
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        for vote in self.votes.all():
            self.rating += vote.value
        self.rating = self.rating/self.votes.count() if self.votes.count() > 0 else 0
        super().save(*args, **kwargs)


class Favourite(models.Model):
    products = models.ManyToManyField('Product')


class Cart(models.Model):
    products = models.ManyToManyField('Product')
