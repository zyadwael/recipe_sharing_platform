from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Recipe, Ingredient, Favorite

# Index (Homepage) view
def index(request):
    # Get all recipes ordered by created_at (newest first)
    recipes = Recipe.objects.all().order_by('-created_at')
    
    # Check if each recipe is a favorite for the current user
    if request.user.is_authenticated:
        favorite_recipes = Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        # Add `is_favorite` to each recipe
        for recipe in recipes:
            recipe.is_favorite = recipe.id in favorite_recipes
    else:
        out = True
        # If not logged in, no favorites
        for recipe in recipes:
            recipe.is_favorite = False
    
    return render(request, 'index.html',{'recipes': recipes})


# Login view
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# Register view
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
    return render(request, 'register.html')

# Logout view
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('index')

# Add Recipe view
@login_required
def add_recipe(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        ingredients_data = request.POST.getlist('ingredients[]')
        quantities_data = request.POST.getlist('quantities[]')
        image = request.FILES.get('image')  # Check for uploaded file

        if title and description and ingredients_data:
            recipe = Recipe.objects.create(
                title=title,
                description=description,
                author=request.user,
                image=image  # Assign the file if uploaded
            )
            for ingredient_name, quantity in zip(ingredients_data, quantities_data):
                Ingredient.objects.create(recipe=recipe, name=ingredient_name, quantity=quantity)

            messages.success(request, "Recipe added successfully!")
            return redirect('my_recipes')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'add_recipe.html')

# My Recipes view
@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'my_recipes.html', {'recipes': recipes})

@login_required
def favorites(request):
    # Get all recipes that are marked as favorites for the logged-in user
    favorite_recipes = Favorite.objects.filter(user=request.user).values_list('recipe', flat=True)
    
    # Get the recipes based on the favorites list
    recipes = Recipe.objects.filter(id__in=favorite_recipes).order_by('-created_at')
    
    # Mark each recipe as favorite
    for recipe in recipes:
        recipe.is_favorite = True  # All these recipes are favorites by the user
    
    return render(request, 'favorites.html', {'recipes': recipes})


# Recipe Detail view
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})

# Toggle Favorite view
from django.http import JsonResponse

@login_required
def toggle_favorite(request, recipe_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if action == 'add':
            Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        elif action == 'remove':
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
