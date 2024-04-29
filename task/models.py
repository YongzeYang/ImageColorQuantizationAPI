from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True) # Task ID
    image_upload_status = models.IntegerField(default=0)
    image_id = models.ForeignKey('image.Image', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    quantization_status = models.IntegerField(default=0)
    quantization_id = models.ForeignKey('quantization.Quantization', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    generation_status = models.IntegerField(default=0)
    generation_id = models.ForeignKey('generation.Generation', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'task'
        app_label = 'task'
        verbose_name = 'task'
        verbose_name_plural = 'tasks'