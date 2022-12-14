# Generated by Django 4.1.1 on 2022-12-20 12:31

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='AbstractContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Product title')),
                ('image', models.ImageField(upload_to='', verbose_name='Product image')),
                ('description', models.TextField(verbose_name='Product description')),
                ('height', models.IntegerField(verbose_name='Product height')),
                ('width', models.IntegerField(verbose_name='Product width')),
                ('length', models.IntegerField(verbose_name='Product length')),
                ('material', models.CharField(max_length=255, verbose_name='Product material')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Product price')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Discount percent')),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, unique=True)),
                ('votes', models.ManyToManyField(to='store.vote')),
            ],
        ),
    ]
