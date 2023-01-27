from django.db import models
from slugify import slugify

from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Products(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    def avg_rating(self):
        from django.db.models import Avg
        result = self.rating.aggregate(Avg('rating'))
        return result['rating__avg']
    

    class Meta:
        ordering = ['-created_at']


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'{self.rating} U {self.author.name} ---> {self.products.title}'


class Reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()

    def __str__(self) -> str:
        return self.body


class Basket(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='basket') 

    def __str__(self) -> str:
        return self.product.title


class Favorite(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self) -> str:
        return self.product.title