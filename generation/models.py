from django.db import models

# Create your models here.
class Generation(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='generations')
    quantization = models.ForeignKey('quantization.Quantization', on_delete=models.CASCADE, related_name='generations')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_image_path = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'generation'
        app_label = 'generation'
        verbose_name = 'generation'
        verbose_name_plural = 'generations'