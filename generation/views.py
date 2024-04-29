from django.shortcuts import render

from rest_framework import viewsets
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from utils.JsonResponse import JsonResponse
from generation.serializers import GenerationSerializer

from generation.models import Generation
from django.http import FileResponse, HttpResponse

class GenerationViewSet(viewsets.ViewSet):
    
    def retrieve(self, request):
        try:
            pk = request.data.get('generation_id')
            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            generation = Generation.objects.get(id = pk)
            # wrong id
            if not generation:
                return JsonResponse(JsonResponse.NOT_GENERATED_YET)
            
            serializer = GenerationSerializer(generation)
            
            return JsonResponse(JsonResponse.SUCCESS, serializer.data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
    
    def download(self, request):
        try:
            pk = request.data.get('generation_id')
            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            generation = Generation.objects.get(id=pk)
            # wrong id
            if not generation:
                return JsonResponse(JsonResponse.INVALID_IMAGE_ID)
            img_path = generation.result_image_path
            with open(img_path, 'rb') as f:
                img_content = f.read()

            response = HttpResponse(img_content, content_type='image/png')
            return response
        
        except FileNotFoundError:
            return JsonResponse(JsonResponse.FILE_NOT_FOUND)
        except Generation.DoesNotExist:
            return JsonResponse(JsonResponse.NOT_GENERATED_YET)
        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))