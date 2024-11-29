from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('login/', views.login, name='login'),  # Login
    path('register/', views.register, name='register'),  # Register
    path('logout/', views.logout, name='logout'),  # Logout
    path('add_recipe/', views.add_recipe, name='add_recipe'),  # Add Recipe
    path('my_recipes/', views.my_recipes, name='my_recipes'),  # My Recipes
    path('favorites/', views.favorites, name='favorites'),  # Favorites
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),  # Recipe Detail
    path('toggle-favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),  # Toggle Favorite
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
