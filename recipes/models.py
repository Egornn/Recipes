from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class CategoryEnum(Enum):
    BREAKFAST = 'Breakfast'
    FIRST_COURSE = 'First Course'
    MAIN = 'Main'
    DESSERT = 'Dessert'
   
class Category(models.Model):
    name = models.CharField(verbose_name='Category Name', max_length=100, choices=[(tag.value, tag.value) for tag in CategoryEnum])

class Recipe(models.Model):
    name = models.CharField(verbose_name='Label', max_length=100)
    cooking_time = models.IntegerField(verbose_name='Time (min)')
    description = models.CharField(verbose_name='Description', max_length=1000)
    steps = models.CharField(verbose_name='Steps', max_length=1000)
    image = models.ImageField(verbose_name='Photo', upload_to='images/')
    create_at = models.DateTimeField(verbose_name='Time', auto_now=True)

class CookingItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)