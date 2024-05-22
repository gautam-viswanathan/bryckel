from rest_framework.views import APIView
from django.http import JsonResponse
from .models import taskManager
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from django.contrib.auth.models import User,Group
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from itertools import groupby
from operator import itemgetter
# Create your views here.

class TaskList(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,format=None):
        try:
            task=taskManager.objects.all()
            serialized_tasks=TaskSerializer(task,many=True)
            tasks_data = serialized_tasks.data
            sorted_tasks = sorted(tasks_data, key=itemgetter("due_date"))
            grouped_tasks = []
            for date, tasks_in_group in groupby(sorted_tasks, key=itemgetter("due_date")):
                grouped_tasks.append({"date": date, "tasks": list(tasks_in_group)})
            return JsonResponse(grouped_tasks, safe=False)
        
        except taskManager.DoesNotExist:
            return JsonResponse({"message":"Could not fetch data"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,format=None):
        try:
            serializer=TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except taskManager.DoesNotExist:
            return JsonResponse({"message":"Can post data"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        for group in Group.objects.all():
            print(group)
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email  })
    
class ListTask(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,id):
        try:
            task=taskManager.objects.get(id=id)
            serializer=TaskSerializer(task)
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        except taskManager.DoesNotExist:
            return JsonResponse({"message":"Could not find the id"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            task=taskManager.objects.get(id=id)
            if task:
                task.delete()
                return JsonResponse({"message":f'Object with ID {id} has been deleted.'},status=status.HTTP_202_ACCEPTED)
            else:
                return JsonResponse({'error': f'Object with ID {id} does not exist.'},status.HTTP_404_NOT_FOUND)
        except taskManager.DoesNotExist:
            return JsonResponse({'error': f'Object with ID {id} does not exist.'},status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        try:
            task = taskManager.objects.get(id=id)
            print(task)
            task.status=True
            serializer = TaskSerializer(task,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except taskManager.DoesNotExist:
            return Response({'error': f'Object with ID {id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(APIView):
    authentication_classes = []
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


