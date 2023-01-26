from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Reviews)
admin.site.register(Basket)
admin.site.register(Favovite)