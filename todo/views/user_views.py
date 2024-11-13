from ..serializers import UserSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def RegisterView(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Data tidak valid',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    first_name = serializer.validated_data.get('first_name')
    last_name = serializer.validated_data.get('last_name')
    password = serializer.validated_data.get('password')
    hashed_password = make_password(password)

    try:
        data_user = User.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            is_active=True
        )

        user_serializer = UserSerializer(data_user)

        return Response({
            'success': True,
            'message': 'Success to register',
            'data': user_serializer.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to register',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def LoginView(request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()
    if not user:
        return Response({
            'success': False,
            'message': 'Username and password is not match',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': 'Username and password is not match'
        }, status=status.HTTP_400_BAD_REQUEST)