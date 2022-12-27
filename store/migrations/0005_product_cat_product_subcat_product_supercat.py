# Generated by Django 4.1.1 on 2022-12-20 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_supercategory_subcategory_category_supercat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcat',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='supercat',
            field=models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.supercategory'),
        ),
    ]