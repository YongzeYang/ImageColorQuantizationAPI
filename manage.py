#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_quantization.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    
    # If you use macOS, you have to setup this
    multiprocessing.set_start_method('fork') 
    
    # Setup your environments
    os.environ['SPARK_HOME'] = 'spark-3.5.1-bin-hadoop3'
    os.environ['HADOOP_HOME'] = 'hadoop-3.3.6'
    
    main()
