# Generated by Django 4.1.1 on 2022-11-19 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_category_supercategory_subcategory_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='supercategory',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='Product price'),
        ),
    ]
