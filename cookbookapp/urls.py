from django.urls import path
from .views import add_product_to_recipe,get_all_products_info,cook_recipe, show_recipes_without_product, show_all_products, show_recipes_without_product_redirect

urlpatterns = [
    path('show_recipes_without_product/<int:product_id>/', show_recipes_without_product, name='show_recipes_without_product'),
    path('show_all_products/', show_all_products, name='show_all_products'),
    path('show_recipes_without_product_redirect/<int:product_id>/', show_recipes_without_product_redirect, name='show_recipes_without_product_redirect'),
    path('cook_recipe/', cook_recipe, name='cook_recipe'),
    path('get_all_products_info/', get_all_products_info, name='get_all_products_info'),
    path('add_product_to_recipe/', add_product_to_recipe, name='add_product_to_recipe'),
]
