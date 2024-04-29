from django.shortcuts import render

from rest_framework import viewsets
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from utils.JsonResponse import JsonResponse
from task.serializers import TaskSerializer
import os
import matplotlib.pyplot as plt
import numpy as np
from django.http import FileResponse, HttpResponse

from image.models import Image
from task.models import Task
from image.serializers import ImageSerializer

class ImageViewSet(viewsets.ViewSet):
        
    def upload_image(self, request):
        try:
            task_id = request.data.get('task_id')

            file = request.FILES.get('image')

            if not all([task_id, file]):
                return JsonResponse(JsonResponse.MISSING_PARAMETERS)

            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return JsonResponse(JsonResponse.TASK_NOT_EXISTS)
            
            try:
                image = plt.imread(file)
            except Exception:
                return JsonResponse(JsonResponse.INVALID_IMAGE_TYPE)
            
            if task.image_upload_status == 10:
                return JsonResponse(JsonResponse.IMAGE_ALREADY_UPLOADED)
        
            # retrieve image attributes
            height = image.shape[0]  # rows
            width = image.shape[1]  # columns
            pixels = height * width # pixels
            if image.shape[2] == 4: # if another channel
                image = image[:, :, :3] # only preserve R,G,B channel
            color_count = len(np.unique(image.reshape(-1, 3), axis=0)) # unique colors
            image_format = file.name.split('.')[-1].lower()

            img_object = Image.objects.create(
                task=task,
                image_path='',  # We'll update this later
                pixel_count=pixels,
                color_count=color_count,
                width=width,
                height=height,
                image_type=image_format,  # Corrected field name
                image_size=file.size / 1024.0,  # Convert to KB
                upload_time=timezone.now()
            )

            # Save the image to the appropriate path
            file_path = os.path.join('workspace', 'images', str(img_object.id), file.name)
            path = default_storage.save(file_path, file)

            # Update the image_path field
            img_object.image_path = path
            img_object.save()

            serializer = ImageSerializer(img_object)

            task.image_id = img_object
            task.image_upload_status = 10
            task.save()

            return JsonResponse(JsonResponse.SUCCESS, serializer.data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
    
    def retrieve(self, request):
        try:
            pk = request.data.get('image_id')
            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            img = Image.objects.get(id=pk)
            # wrong id
            if not img:
                return JsonResponse(JsonResponse.INVALID_IMAGE_ID)

            serializer = ImageSerializer(img)
            return JsonResponse(JsonResponse.SUCCESS, serializer.data)
        except Image.DoesNotExist:
            return JsonResponse(JsonResponse.INVALID_IMAGE_ID)
        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
        
    def download(self, request):
        try:
            pk = request.data.get('image_id')
            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            img = Image.objects.get(id=pk)
            # wrong id
            if not img:
                return JsonResponse(JsonResponse.INVALID_IMAGE_ID)
            img_path = img.image_path
            with open(img_path, 'rb') as f:
                img_content = f.read()

            response = HttpResponse(img_content, content_type='image/jpeg')
            return response
        
        except FileNotFoundError:
            return JsonResponse(JsonResponse.FILE_NOT_FOUND)
        except Image.DoesNotExist:
            return JsonResponse(JsonResponse.INVALID_IMAGE_ID)
        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
        
