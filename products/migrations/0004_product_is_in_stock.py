# Generated by Django 5.0.6 on 2024-06-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_ordered_date_order_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
