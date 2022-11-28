from django.db import models


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    logo = models.CharField(max_length=250, blank=True, null=True)
    active = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'categories'


class Brand(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    active = models.IntegerField(default=1, blank=False, null=False)
    logo = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'brand'


class Products(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='product_category_rel', on_delete=models.CASCADE)
    logo = models.CharField(max_length=250, blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='product_brand_rel',
                              on_delete=models.PROTECT)
    active = models.IntegerField(default=1)
    deleted = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    class Meta:
        managed = True
        db_table = 'products'


class ProductReview(models.Model):
    product = models.ForeignKey(Products, on_delete=models.PROTECT,
                                related_name='product_review_product_id_rel')
    max = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    comment = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product_review'
