from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminAuthPermission, IsAuthorPermission
from rest_framework.permissions import AllowAny
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

