from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('todos/', views.TodoListView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
]
