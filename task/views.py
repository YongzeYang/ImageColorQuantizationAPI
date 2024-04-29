from django.shortcuts import render
from rest_framework import viewsets
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from utils.JsonResponse import JsonResponse
from task.serializers import TaskSerializer
import os

from task.models import Task

class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)

            return JsonResponse(JsonResponse.SUCCESS, serializer.data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
        
    def create(self, request):
        try:
            task = Task.objects.create()
            serializer = TaskSerializer(task)

            return JsonResponse(JsonResponse.SUCCESS, serializer.data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
    
    def retrieve(self, request):
        try:
            pk = request.data.get('task_id')
            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            task = Task.objects.get(id=pk)
            # wrong id
            if not task:
                return JsonResponse(JsonResponse.TASK_NOT_EXISTS)

            serializer = TaskSerializer(task)
            return JsonResponse(JsonResponse.SUCCESS, serializer.data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))