# Generated by Django 4.1 on 2024-04-26 23:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quantization", "0003_quantization_method"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quantization",
            name="actual_iterations",
        ),
        migrations.RemoveField(
            model_name="quantization",
            name="iterations",
        ),
        migrations.AddField(
            model_name="quantization",
            name="arg1",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="quantization",
            name="arg2",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="quantization",
            name="arg3",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="quantization",
            name="arg4",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]