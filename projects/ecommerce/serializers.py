from datetime import datetime
from decimal import Decimal

from rest_framework import serializers
from rest_framework.utils import json
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = "__all__"


class ProductGenericSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    logo = serializers.CharField()
    type = serializers.IntegerField()
    review_max = serializers.DecimalField(max_digits=16, decimal_places=2)
    review_value = serializers.DecimalField(max_digits=16, decimal_places=2)
    review_avg_max = serializers.DecimalField(max_digits=16, decimal_places=2)
    review_avg_value = serializers.DecimalField(max_digits=16, decimal_places=2)
    category_data = serializers.JSONField()
    brand_data = serializers.JSONField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'price': instance.price,
            'description': instance.description,
            'logo': instance.logo,
            # 'review_max': instance.review_max_data,
            # 'review_value': instance.review_value_data,
            # 'review_avg_max': instance.review_avg_max_data,
            # 'review_avg_value': instance.review_max_value_data,
            'category_data': instance.category_data,
            'brand_data': instance.brand_data,
        }
