# Image Quantization API

## Introduction

This project is part of a group assignment for CityU CS5296 Cloud Computing:Theo & Prac.

We provide PySpark-based image quantization with support for using different algorithms (e.g., kMeans) with different parameters (e.g., number of colors k, maximum number of iterations maxIter, etc.). This project references the previous project (https://github.com/YongzeYang/Parallel-Color-Quantization). However, we rewrote all the code and refactored all the logic (the previous project had only simple Java and Scala scripts). We provided a complete webserver implementation that supports users to access our service by initiating HTTP requests through a browser or an interface management tool (e.g. Postman).

The project consists of both front-end and back-end components, and this repository contains the complete back-end Django code. To run it, make sure you have the Python Django environment and Spark environment installed on your device.

## To start our server

### Environments
This project used Apache Spark for parallel computing, so make sure you have Spark installed on your computer, you can refer to the official Spark website: https://spark.apache.org/downloads.html.

We assume that you have Python installed on your computer and you can use our requirements.txt to install the required environment. First, you need to activate your virtual environment (if any):

```bash
$ source venv/bin/activate
```

The necessary environments required to run this project are Django, Django Restful Framework, PySpark, NumPy, Pandas, Pillow, matplotlib, etc. You can use the following command to install the required environment:

```bash
$ pip install -r requirements.txt
```

Of course, you can also modify the version number and environment dependencies yourself. 

### Configurations

Normally, you don't need to do a database migration because we use sqlite for our database. if you need to do a database migration, you can run the following command:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

The database is configured in `image_quantization/settings.py`. You can change your database to MySQL, PostgreSQL, etc. according to your actual needs

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Before starting our service, you need to modify other configurations to suit your situation. In `manage.py`, we set the environment variables for Hadoop and Spark:    

```python
# Setup your environments
os.environ['SPARK_HOME'] = 'spark-3.5.1-bin-hadoop3'
os.environ['HADOOP_HOME'] = 'hadoop-3.3.6'
```

In addition, if you are running macOS, you need to add the following additional statement:

``` python
# If you use macOS, you have to setup this
multiprocessing.set_start_method('fork') 
```

### Start Django Service
When everything is ready, you can run the following command to turn on the Django service:

```bash
$ python manage.py runserver 8000
```

It will run on port 8000 by default. You can change the port number as per your requirement.