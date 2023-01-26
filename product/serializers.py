from rest_framework import serializers
from django.db.models import Avg

from account.serializers import RegistrationSerializer
from .models import Category, Rating, Products, Reviews


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    # category = serializers.ManyRelatedField()

    class Meta:
        model = Rating
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def validate_rating(self, rating):
        if rating > 5:
            raise serializers.ValidationError('слишком много, выберите рейтинг от 1 до 5')
        elif rating < 1:
            raise serializers.ValidationError('cлишком мало, выберите рейтинг от 1 до 5')
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)
    

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')


    class Meta:
        model = Reviews
        fields = '__all__'

    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        reviews = Reviews.objects.create(author=user, **validated_data)
        return reviews

    def update(self, instance, validated_data):
        instance.reviews = validated_data.get('reviews')
        instance.save()
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    number = serializers.ReadOnlyField(source='author.phone_number')
    

    class Meta:
        model = Products
        fields = [ 'title', 'price', 'descriptions', 'image', 'category', 'author', 'number']
        # fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = Products.objects.create(author=user, **validated_data)
        return product

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Такой продукт уже существует')
        return title
    
    def validate_number(self, number):
        if len(number) > 13 or not number.is_digit():
            raise serializers.ValidationError('неправильный формат номера, пример: 0700934445')
        return number

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(Reviews.objects.filter(product=instance.pk), many=True).data
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        return representation


    
class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'
