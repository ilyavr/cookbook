from django.db import models
from django.core.exceptions import ValidationError
class Product(models.Model):
    name = models.CharField(max_length=255)
    times_used = models.IntegerField(default=0)
    used_in_recipes = models.IntegerField(default=0)

    def __str__(self):
        return self.name
        

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, through='RecipeProduct')

    def __str__(self):
        return self.name

class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.weight}g) in {self.recipe.name}"
    def clean(self):
        if self.weight < 1:
            raise ValidationError('weight should not be less than 1')
    
