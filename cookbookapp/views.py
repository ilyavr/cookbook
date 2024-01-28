from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Recipe, Product, RecipeProduct
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging


@receiver(post_save, sender=RecipeProduct)

def update_used_in_recipes(sender, instance, **kwargs):
    product = instance.product
    product.used_in_recipes = RecipeProduct.objects.filter(product=product).count()
    product.save()

logger = logging.getLogger(__name__)

def add_product_to_recipe(request):
    if request.method == 'GET':
        try:
            recipe_id = int(request.GET.get('recipe_id'))
            product_id = int(request.GET.get('product_id'))
            weight = float(request.GET.get('weight'))
            recipe = get_object_or_404(Recipe, id=recipe_id)
            product = get_object_or_404(Product, id=product_id)
            recipe_product, created = RecipeProduct.objects.get_or_create(recipe=recipe, product=product, defaults={'weight': weight})

            if not created:
                recipe_product.weight = weight

            recipe_product.save()

            return JsonResponse({'status': 'success', 'weight': recipe_product.weight})
        except Exception as e:
            logger.error(f'Ошибка add_product_to_recipe: {str(e)}')


def cook_recipe(request):

    if request.method == 'GET':
        recipe_id = request.GET.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        for recipe_product in recipe.recipeproduct_set.all():
            product = recipe_product.product
            product.times_used += 1
            product.save()
        return JsonResponse({'status': 'success', 'times_used': product.times_used})

def get_all_products_info(request):
    products_info = [{'product_id': product.id, 'times_used': product.times_used} for product in Product.objects.all()]

    return JsonResponse({'products_info': products_info})

def show_all_products(request):

    products = Product.objects.all()
    unique_recipes = Recipe.objects.all().distinct()
    context = {'products': products, 'unique_recipes': unique_recipes}

    return render(request, 'all_products.html', context)

def show_recipes_without_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    recipes_without_product = Recipe.objects.filter(~Q(recipeproduct__product=product)).distinct()
    recipes_with_low_weight = Recipe.objects.filter(recipeproduct__product=product, recipeproduct__weight__lt=10).distinct()
    recipes = recipes_without_product | recipes_with_low_weight
    context = {'recipes': recipes, 'product': product}

    return render(request, 'recipes_without_product.html', context)

def show_recipes_without_product_redirect(request, product_id):
    return redirect('show_recipes_without_product', product_id=product_id)

