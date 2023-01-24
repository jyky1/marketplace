from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


from .serializers import RatingSerializer, CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Rating, Category, Products, Reviews

# Create your views here.

class RatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    
class ReviewsView(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

