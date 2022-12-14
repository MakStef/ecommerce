# Generated by Django 4.1.1 on 2022-12-20 13:18

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_vote_user'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cart',
            field=models.OneToOneField(default=store.models.Cart.get_new, on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Products in cart'),
        ),
        migrations.AddField(
            model_name='account',
            name='favourite',
            field=models.OneToOneField(default=store.models.Favourite.get_new, on_delete=django.db.models.deletion.CASCADE, to='store.favourite', verbose_name='Favourite products'),
        ),
    ]
