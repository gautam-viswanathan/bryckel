from django.contrib import admin
from django.urls import path
from .views import ListUsers,CustomAuthToken,TaskList,ListTask,UserCreate



urlpatterns=[path('tasks/',TaskList.as_view()),
             path('api/users/', ListUsers.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('task/<int:id>/',ListTask.as_view()),
    path('create/',UserCreate.as_view())
]