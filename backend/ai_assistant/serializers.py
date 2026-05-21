from rest_framework import serializers
from base.models import Product


class ChatProductSerializer(serializers.ModelSerializer):
    """Lightweight serializer for products returned in chat responses."""

    class Meta:
        model = Product
        fields = [
            "_id",
            "name",
            "brand",
            "category",
            "price",
            "countInStock",
            "image",
            "description",
        ]
