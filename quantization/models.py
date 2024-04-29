from django.db import models

# Create your models here.
class Quantization(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='quantizations')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    result_file_path = models.CharField(max_length=500, null=True, blank=True)
    k = models.IntegerField()
    
    method = models.CharField(max_length=20, null=True, blank=True)
    arg1 = models.CharField(max_length=20, null=True, blank=True) # maxIter, for most of the cases
    arg2 = models.CharField(max_length=20, null=True, blank=True)
    arg3 = models.CharField(max_length=20, null=True, blank=True)
    arg4 = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'quantization'
        app_label = 'quantization'
        verbose_name = 'quantization'
        verbose_name_plural = 'quantizations'