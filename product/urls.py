from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryView, ReviewsView, ProductView, RatingView, FavoriteView, BasketView


router = DefaultRouter()
router.register('products', ProductView)
router.register('reviews', ReviewsView)
router.register('rating', RatingView)
router.register('favorite', FavoriteView)
router.register('basket', BasketView)



urlpatterns = [
    path('categories/', CategoryView.as_view({'get':'list'})),
    path('', include(router.urls)),
]