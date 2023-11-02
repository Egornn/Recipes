from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_main, name='main'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.register, name='register'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('category_edit/<int:item_id>', views.edit_category_by_id, name='category-edit'),
    path('recipes/', views.get_recipes, name='recipes'),
    path('user_recipes/', views.get_user_recipes, name='get_user_recipes'),
    path('user_recipe_detail/<int:item_id>', views.get_user_recipe_by_id, name='user_recipe-detail'),
    path('recipe_detail/<int:item_id>', views.get_detail_recipe_by_id, name='recipe-detail'),
    path('recipe_delete/<int:item_id>', views.delete_cooking_item_by_id, name='recipe-delete'),
    path('recipe_edit/<int:item_id>', views.edit_recipe_by_id, name='recipe-edit'),
]
