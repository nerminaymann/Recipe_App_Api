from django.urls import path,include
import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('recipes',views.RecipeView)

app_name = 'recipe'

path('', include(router.urls)),