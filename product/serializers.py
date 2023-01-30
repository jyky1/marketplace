from rest_framework import serializers
from django.db.models import Avg

from account.models import User

from .models import Category, Rating, Products, Reviews, Favorite, Basket


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    

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
    
    

    class Meta:
        model = Products
        fields = [ 'title', 'price', 'descriptions', 'image', 'category', 'author']
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

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product')
        instance.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(Reviews.objects.filter(product=instance.pk), many=True).data
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        # representation['favorit_count'] = instance.favorit.count()
        return representation

    
# class ProductListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Products
#         fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class FavoritSerializer(serializers.ModelSerializer):


    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        favorite = Favorite.objects.create(**validated_data)
        return favorite

    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('Такой продукт уже существует в избранных')
        return product


    def update(self, instance, validated_data):
        instance.favorit = validated_data.get('favorite')
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance, validated_data):
        instance.favorit = validated_data.get('favorite')
        instance.save()
        return validated_data.pop(instance.favorite)

<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes

class BasketSerializer(serializers.ModelSerializer):


    class Meta:
        model = Basket
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     print(f'->{instance}<-')
    #     print(f'-#{self}#-')
    #     representation['price'] = ProductSerializer(Products.objects.filter(products_id=), many=True).data
    #     return representation


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        basket = Basket.objects.create(**validated_data)
        return basket

    def validate_product(self, product):
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError('Такой продукт уже сушествует в корзине')
        return product

    def update(self, instance, validated_data):
        instance.basket = validated_data.get('basket')
        instance.save()
        return super().update(instance, validated_data)

    def delete(self, instance, validated_data):
        instance.basket = validated_data.get('basket')
        instance.save()
        return validated_data.pop(instance.basket)