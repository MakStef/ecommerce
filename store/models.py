from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from abc import ABCMeta, abstractmethod
import uuid


User = settings.AUTH_USER_MODEL


# Create new Meta class and ABCmodel for future abstractmethods handling
class AbstractModelMeta(ABCMeta, type(models.Model)):
    pass


class ABCModel(models.Model):
    __metaclass__ = AbstractModelMeta

    class Meta:
        abstract = True


# Models
class AbstractContainer(ABCModel):
    """ Abstract class to define the get_new container function for ForeignKey fields default. """
    @classmethod
    def get_new(cls):
        return cls.objects.create().id



class AbstractProductContainer(AbstractContainer):
    """ Abstract container for products. """
    products = models.ManyToManyField('Product')

    def toggle(self, product):
        if self.products.all().contains(product):
            self.products.remove(product)
            return False
        else:
            self.products.add(product)
            return True

class Favourite(AbstractProductContainer):
    """ Product container for saving products. """
    pass


class Cart(AbstractProductContainer):
    """ Product container for purchasing products. """
    pass

 
class Vote(models.Model):
    """ User vote for a product. """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        editable=False,
        default=None,
    )
    value = models.FloatField(
        editable=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )


class Product(models.Model):
    """ 
        Product model. title: str, image: file, description: str, height,width,length: int, material: str,
        price: float, discount: int(1...100), subcat: Subcategory, cat: Category, supercat: Supercategory.
        Has votes and defines rate.
    """
    title = models.CharField(verbose_name="Product title", max_length=255)
    image = models.ImageField(verbose_name="Product image") 
    description = models.TextField(verbose_name="Product description")
    height = models.IntegerField(verbose_name="Product height")
    width = models.IntegerField(verbose_name="Product width")
    length = models.IntegerField(verbose_name="Product length")
    material = models.CharField(verbose_name="Product material", max_length=255)
    price = models.FloatField(verbose_name="Product price", validators=[MinValueValidator(0)])
    discount = models.IntegerField(
        verbose_name="Discount percent",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    subcat = models.ForeignKey('Subcategory', on_delete=models.CASCADE, default=None)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, editable=False, null=True, default=None)
    supercat = models.ForeignKey('Supercategory', on_delete=models.CASCADE, editable=False, null=True, default=None)

    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    sold = models.PositiveIntegerField(editable=False, default=0)
    votes = models.ManyToManyField('Vote')
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False,)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.cat = self.subcat.cat
        self.supercat = self.cat.supercat

        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def rate(self, rating: int, user: User):
        vote, is_new = self.votes.get_or_create(
            user=user,
            defaults={
                'user': user,
                'value': rating,
            }
        )
        if not is_new:
            vote.value = rating

        vote.save()
        return vote.value

    def get_rating(self):
        """ Returns the rating of product. \n\nPrecision of the fraction is two numbers """
        votes = self.votes.all().values_list('value', flat=True)
        return float(f'{sum(votes) / len(votes):.2f}') if len(votes) > 0 else 0


class AbstractCategory(ABCModel):
    """ 
        Categories ancestor with fields of title, slug and created_at timestamp. 
        Creates slug on save, orders categories by created_at, 
        return title as representative, defines get_absolute_url.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False,)
    created_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        """ Create slug, created_at and saves object """
        if not self.id:
            created_at = timezone.now()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @abstractmethod
    def get_products(self, ordering:str=None):
        """ Get Products QuerySet filtered by category and ordered by ordering """
        return Product.objects.filter(abscat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])

    @abstractmethod
    def get_absolute_url(self):
        """ Get absolute url to filter by category """
        return f"{reverse('store:products')}?abscat='{self.slug}'"

    def __str__(self):
        return self.title


class Subcategory(AbstractCategory):
    cat = models.ForeignKey('Category', models.CASCADE)

    def get_absolute_url(self):
        return f"{reverse('store:products')}?subcategory_id={self.id}"

    def get_products(self, ordering:str=None):
        return Product.objects.filter(subcat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])

class Category(AbstractCategory):
    supercat = models.ForeignKey('Supercategory', models.CASCADE)

    def get_absolute_url(self):
        return f"{reverse('store:products')}?category_id={self.id}"

    def get_products(self, ordering:str=None):
        return Product.objects.filter(cat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])

    def get_subcats(self, ordering:str=None):
        return Subcategory.objects.filter(cat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])


class Supercategory(AbstractCategory):

    def get_products(self, ordering:str=None):
        return Product.objects.filter(supercat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])

    def get_cats(self, ordering:str=None):
        return Category.objects.filter(supercat_id=self.id).order_by(ordering if ordering else self._meta.ordering[0])
    
    def get_absolute_url(self):
        return f"{reverse('store:products')}?supercategory_id={self.id}"