# Generated by Django 4.1.3 on 2022-11-28 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerce", "0002_products_price_alter_products_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productreview",
            name="value",
        ),
    ]