from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'image_upload_status', 'image_id',
                  'quantization_status', 'quantization_id', 'generation_status',
                  'generation_id', 'created_at']
