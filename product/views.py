from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminAuthPermission, IsAuthorPermission
from rest_framework.permissions import AllowAny
from .serializers import RatingSerializer, CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Rating, Category, Products, Reviews
from rest_framework.pagination import PageNumberPagination

from .serializers import RatingSerializer, CategorySerializer, ProductSerializer, ReviewSerializer, BasketSerializer, FavoritSerializer
from .models import Rating, Category, Products, Reviews, Favorite, Basket

# Create your views here.

class RatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5

class ProductView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    pagination_class =ProductListPagination



    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]

        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return [permission() for permission in self.permission_classes]
    
class ReviewsView(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


class FavoritView(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritSerializer


class BasketView(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer