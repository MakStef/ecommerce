# Generated by Django 4.1.1 on 2022-12-24 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
