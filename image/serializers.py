from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'task', 'pixel_count', 'color_count', 'width', 'height', 'image_type', 'image_size', 'upload_time')
