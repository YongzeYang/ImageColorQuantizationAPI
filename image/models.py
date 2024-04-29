from django.db import models
from django.utils import timezone

# Create your models here.
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=500)
    pixel_count = models.IntegerField()
    color_count = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    image_type = models.CharField(max_length=50)
    image_size = models.FloatField() # kb
    upload_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'image'
        app_label = 'image'
        verbose_name = 'image'
        verbose_name_plural = 'images'