from rest_framework import serializers

from .models import Category, Rating, Products, Reviews


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Reviews
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Products
        fields = '__all__'