from django.urls import path
from django.contrib.auth import get_user_model
from .views import CreateUserView

User = get_user_model()
app_name = 'user'

urlpatterns = [
    path('create/',CreateUserView.as_view(),name='create'),
]