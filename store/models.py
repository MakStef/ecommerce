from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

from abc import ABCMeta, abstractmethod


User = settings.AUTH_USER_MODEL


# Create new Meta class and ABCmodel for future abstractmethods handling
class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ABCModel(models.Model):
    __metaclass__ = AbstractModelMeta

    class Meta:
        abstract = True


# Managers
class ProductContainersManager(models.Manager):
    def toggle_product(self, product):
        self.products.remove(product) if self.products.contains(
            product) else self.products.add(product)


# Models
class AbstractContainer(ABCModel):

    @classmethod
    def get_new(cls):
        return cls.objects.create().id


class Favourite(AbstractContainer):
    """ Product container for saving products. """
    products = models.ManyToManyField('Product')

    objects = ProductContainersManager()


class Cart(AbstractContainer):
    """ Product container for purchasing products. """
    products = models.ManyToManyField('Product')

    objects = ProductContainersManager()


class Vote(models.Model):
    """ User vote for a product. """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        editable=False
    )
    value = models.FloatField(
        editable=False,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )


class Product(models.Model):
    """ Product model. *title: str, *image: file, *description: str, *price: float  """
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
    price = models.FloatField(verbose_name="Product price")
    subcategory = models.ForeignKey(
        to='ProductSubcategory',
        on_delete=models.CASCADE,
        editable=True,
        null=True,
    )
    category = models.ForeignKey(
        to='ProductCategory',
        on_delete=models.CASCADE,
        editable=False,
        blank=True,
        default=None
    )
    supercategory = models.ForeignKey(
        to='ProductSuperCategory',
        on_delete=models.CASCADE,
        editable=False,
        blank=True,
        default=None
    )

    votes = models.ManyToManyField('Vote')
    slug = models.SlugField(unique=True, editable=False)

    def rate(self, rating: int):
        try:
            vote, is_new = self.votes.get_or_create(
                user=self.user,
                defaults={
                    'user': self.user,
                    'value': rating,
                }
            )
            if not is_new:
                vote.value = rating

            vote.save()
            return True
        except:
            return False

    def get_rating(self):
        """ Returns the rating of product. \n\nPrecision of the fraction is two numbers """

        votes = self.votes.all().values_list('value', flat=True)
        return float(f'{sum(votes) / len(votes):.2f}') if len(votes) > 0 else 0

    def save(self, *args, **kwargs):
        """ On save creates slug and adds to it "_" + 3 letters of it's category title. """

        self.slug = f'{slugify(self.title)}_{self.category.title[:3]}'

        self.category = self.subcategory.category
        self.supercategory = self.category.supercategory

        super().save(*args, **kwargs)


class AbstractCategory(ABCModel):
    """ 
        Categories ancestor with only fields of title and slug. Creates slug on save,
        orders categories by title, return title as representative, gets absolute url,
        defines get_products abstractmethod.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, default=None, editable=False, )

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        """ Save and create slug. """

        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """ Get absolute url to filter by category """
        return reverse('store:filter', args=(self.slug,))

    @abstractmethod
    def get_products(self):
        """ Get products for this category """
        return Product.objects.filter(abscat_id=self.id)

    def __str__(self):
        return self.title


class ProductSubcategory(AbstractCategory):
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)

    def get_products(self):
        return Product.objects.filter(subcategory_id=self.id)


class ProductCategory(AbstractCategory):
    supercategory = models.ForeignKey(
        'ProductSupercategory',
        on_delete=models.CASCADE
    )

    def get_subcategories(self):
        return ProductSubcategory.objects.filter(category_id=self.id)

    def get_products(self):
        return Product.objects.filter(category_id=self.id)


class ProductSupercategory(AbstractCategory):
    def get_categories(self):
        return ProductCategory.objects.filter(supercategory_id=self.id)

    def get_products(self):
        return Product.objects.filter(supercategory_id=self.id)
