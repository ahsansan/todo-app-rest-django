from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Todo, User
from .serializers import UserSerializer, TodoSerializer
from rest_framework.permissions import IsAuthenticated

# Register User
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

# Login and generate token
class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Todo Views
class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(created_by=self.request.user)
    
# View untuk membuat todo baru
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]  # Hanya bisa diakses jika user login

    def perform_create(self, serializer):
        # Tentukan user yang membuat todo sebagai `created_by`
        serializer.save(created_by=self.request.user, is_completed=False)

# View untuk update data
class TodoUpdateView(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'put']

    def get_object(self):
        # Ambil todo berdasarkan id dan pastikan user adalah pemiliknya
        todo = super().get_object()
        if todo.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to update this todo.")
        return todo
