from django.urls import path
from ..views.todo_views import GetAllTodos, CreateTodo, CompleteTodo, DeleteTodo

urlpatterns = [
    path('', GetAllTodos, name='all_todos'),
    path('add/', CreateTodo, name='add_todos'),
    path('<int:id_edit>/completed/', CompleteTodo, name='complete_todos'),
    path('<int:id_delete>/delete/', DeleteTodo, name='delete_todos'),
]