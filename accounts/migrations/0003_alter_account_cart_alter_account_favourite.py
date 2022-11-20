# Generated by Django 4.1.1 on 2022-11-20 10:56

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_category_product_subcategory_and_more'),
        ('accounts', '0002_account_cart_account_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cart',
            field=models.OneToOneField(default=store.models.Cart.get_new, on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Products in cart'),
        ),
        migrations.AlterField(
            model_name='account',
            name='favourite',
            field=models.OneToOneField(default=store.models.Favourite.get_new, on_delete=django.db.models.deletion.CASCADE, to='store.favourite', verbose_name='Favourite products'),
        ),
    ]