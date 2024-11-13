from django.urls import include, path

urlpatterns = [
    path('user/', include('todo.urls.user_urls')),
    path('todo/', include('todo.urls.todo_urls')),
]