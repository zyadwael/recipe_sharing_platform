from django.contrib import admin
from .models import Recipe, Ingredient, Favorite

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    inlines = [IngredientInline]

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'added_at')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
