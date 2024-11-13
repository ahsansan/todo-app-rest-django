from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from ..serializers import TodoSerializer, AddTodoSerializer
from ..models import Todo

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllTodos(request):
    user = request.user

    if not user:
        return Response({
            'success': False,
            'message': 'Can not access todo'
        }, status=status.HTTP_404_NOT_FOUND)
    
    try:
        todos = Todo.objects.filter(created_by_id=user)
        todo_seq = TodoSerializer(todos, many=True)
        return Response({
            'success': True,
            'message': 'Success get data',
            'data': todo_seq.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to get data',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTodo(request):
    user = request.user

    if not user:
        return Response({
            'success': False,
            'message': 'Can not access todo'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AddTodoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Data is not valid',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data

    try:
        data_todo = Todo.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            is_completed=False,
            created_by_id=user.id
        )

        todo_seq = TodoSerializer(data_todo)

        return Response({
            'success': True,
            'message': 'Success add data',
            'data': todo_seq.data
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to add todo',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def CompleteTodo(request, id_edit):
    user = request.user

    if not user:
        return Response({
            'success': False,
            'message': 'Can not access todo'
        }, status=status.HTTP_404_NOT_FOUND)
    
    todo = Todo.objects.filter(id=id_edit).first()

    if not todo:
        return Response({
            'success': False,
            'message': 'Todo not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if todo.created_by != user:
        return Response({
            'success': False,
            'message': 'Can not update todo'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        todo.is_completed = True
        todo.save()

        return Response({
            'success': True,
            'message': 'Success update data'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to update todo',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteTodo(request, id_delete):
    user = request.user

    if not user:
        return Response({
            'success': False,
            'message': 'Can not access todo'
        }, status=status.HTTP_404_NOT_FOUND)
    
    todo = Todo.objects.filter(id=id_delete).first()

    if not todo:
        return Response({
            'success': False,
            'message': 'Todo not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if todo.created_by != user:
        return Response({
            'success': False,
            'message': 'Can not delete todo'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        todo.delete()

        return Response({
            'success': True,
            'message': 'Success delete data'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to delete todo',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)