from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    pass  # Anda bisa menambahkan atribut lain sesuai kebutuhan, seperti profil, dll.

# Todo model
class Todo(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
