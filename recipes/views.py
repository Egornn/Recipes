from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from recipes.forms import RecipeForm, LoginForm, UserRegistrationForm, CategoryForm, CookingForm
from recipes.models import Recipe, Category, CookingItem
import logging
import random

# Create your views here.
logger = logging.getLogger(__name__)


def get_main(request):
    title = 'Main page'
    recipes = Recipe.objects.all()  
    random_recipes = random.sample(list(recipes), 5)  
    users_count = User.objects.all().count()
    recipes_count = Recipe.objects.all().count()
    return render(request, 'main.html', {'title': title,'users_count': users_count,'recipes_count': recipes_count,'random_recipes': random_recipes})


def get_recipes(request):
    title = 'All recipes'
    items = CookingItem.objects.all().order_by('-recipe_id__create_at')
    return render(request, 'items.html', {'title': title, 'items': items})


def get_user_recipe_by_id(request, item_id: int):
    cooking_item = CookingItem.objects.get(pk=item_id)
    return render(request, 'user_item.html', {'cooking_item': cooking_item})


def get_detail_recipe_by_id(request, item_id: int):
    cooking_item = CookingItem.objects.get(pk=item_id)
    title = cooking_item.recipe_id.name
    return render(request, 'detail_cooking_item.html', {'title': title, 'cooking_item': cooking_item})


def edit_recipe_by_id(request, item_id: int):
    cooking_item = CookingItem.objects.get(pk=item_id)
    title = f'Change Recipe'
    if request.method == 'GET':
        recipe_form = RecipeForm(instance=cooking_item.recipe_id)
        return render(request, 'form.html', {'form': recipe_form, 'title': title})
    elif request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=cooking_item.recipe_id)
        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, 'recipe saved')
            return redirect('get_user_recipes')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'form.html', {'form': recipe_form, 'title': title})


def edit_category_by_id(request, item_id: int):
    cooking_item = CookingItem.objects.get(pk=item_id)
    title = f'Update category'
    if request.method == 'GET':
        category_form = CategoryForm(instance=cooking_item.category_id)
        return render(request, 'form.html', {'form': category_form, 'title': title})
    elif request.method == 'POST':
        category_form = CategoryForm(request.POST, instance=cooking_item.category_id)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'category saved')
            return redirect('get_user_recipes')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'form.html', {'form': category_form, 'title': title})


def delete_cooking_item_by_id(request, item_id: id):
    cooking_item = CookingItem.objects.get(pk=item_id)
    if cooking_item:
        cooking_item.delete()
        messages.success(request, 'Recipe deleted')
    else:
        messages.error(request, 'Recipe not found')
    return redirect('get_user_recipes')

def get_user_recipes(request):
    title = "My recipes"
    full_items = CookingItem.objects.filter(user_id=request.user).order_by('-recipe_id__create_at')
    if not full_items:
        messages.info(request, f'You need to create a reciepe first')
        return redirect('/')
    return render(request, 'full_items.html', {'title': title, 'full_items': full_items,
                                                       'username': request.user.username})


def add_recipe(request):
    title = 'Add recipe'
    head_title = 'Add recipe:'
    cooking_form = CookingForm(request.POST, request.FILES)
    if request.method == 'GET':
        return render(request, 'form.html',{'form': cooking_form,'title': title,'head_title': head_title})
    elif request.method == 'POST':
        if cooking_form.is_valid():
            name = cooking_form.cleaned_data['name']
            category = cooking_form.cleaned_data['category']
            description = cooking_form.cleaned_data['description']
            steps = cooking_form.cleaned_data['steps']
            cooking_time = cooking_form.cleaned_data['cooking_time']
            image = cooking_form.cleaned_data['image']
            recipe = Recipe(name=name, description=description, steps=steps, cooking_time=cooking_time, image=image)
            category = Category(name=category)
            recipe.save()
            category.save()
            cooking_item = CookingItem(user_id=request.user, recipe_id=recipe, category_id=category)
            cooking_item.save()
            messages.success(request, f'Recipe is saved. Thank you {request.user}!')
            return redirect('get_user_recipes')
    else:
        messages.error(request, f'Error. {request.user}')
        return render(request, 'form.html',{'form': cooking_form,'title': title,'head_title': head_title})
    return render(request, 'form.html',{'form': cooking_form,'title': title,'head_title': head_title})


def sign_in(request):
    title = 'Login'

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'title': title})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back {username.title()}!')
                return redirect('main')

    messages.error(request, f'Wrong Login/Password')
    return render(request, 'login.html', {'form': form, 'title': title})


def register(request):
    title = 'Sign up'
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, f'Regitration is successfull')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form, 'title': title})


def sign_out(request):
    title = "Logout"
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, f'Goodbye!')
        return render(request, 'logout.html', {'title': title})
    else:
        return redirect('login')
