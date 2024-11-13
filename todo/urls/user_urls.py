from django.urls import path
from ..views.user_views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
]