from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('todos/create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('todos/', views.TodoListView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('todos/<int:pk>/update/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('todos/<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
]
