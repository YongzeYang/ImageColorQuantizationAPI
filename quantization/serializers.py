from rest_framework import serializers
from .models import Quantization

class QuantizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantization
        fields = ('id', 
                  'task', 
                  'start_time', 
                  'end_time', 
                  'k', 'method', 
                  'arg1', 'arg2', 
                  'arg3', 'arg4')
