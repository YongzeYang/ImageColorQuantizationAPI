from django.shortcuts import render

from rest_framework import viewsets
from django.core.files.storage import default_storage
from utils.JsonResponse import JsonResponse
import os
import matplotlib.pyplot as plt
import numpy as np
from django.utils import timezone
from PIL import Image

from task.models import Task
from quantization.models import Quantization
from quantization.serializers import QuantizationSerializer
from generation.models import Generation

import os
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np

from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans, BisectingKMeans, GaussianMixture
from pyspark.ml.feature import VectorAssembler

def save_image_safely(reshaped_array, generation_path):
    # save image in a subprocess
    print(reshaped_array.shape)
    if np.any(reshaped_array > 1):
        reshaped_array = reshaped_array.astype(np.uint8)
    else:
        reshaped_array = (reshaped_array * 255).astype(np.uint8)
    
    image = Image.fromarray(reshaped_array)
    image.save(generation_path)

def kmeans(task, quantization, path, k, maxIter, tol, initSteps, distanceMeasure):
    
    print("[Quantization] Start K-Means")
    try:
        spark = SparkSession.builder.appName("KMeans").getOrCreate()
        image = plt.imread(path)  # (1154, 802, 4)
        
        # generate spark data frame
        if image.shape[2] == 4:
            image = image[:, :, :3]
        image = image.reshape(-1, 3)
        data_df = spark.createDataFrame(image.tolist(), ["feature1", "feature2", "feature3"])
        assembler = VectorAssembler(inputCols=["feature1", "feature2", "feature3"], outputCol="features")
        data_df = assembler.transform(data_df)

        # generate spark kmeans model
        kmeans = KMeans().setK(int(k)).setMaxIter(int(maxIter)).setTol(float(tol)).setInitSteps(int(initSteps)).setDistanceMeasure(str(distanceMeasure))
        model = kmeans.fit(data_df)
        centers = model.clusterCenters()

        quantization_path = quantization.result_file_path
        quantization_dir = os.path.join('workspace', 'quantization', str(quantization.id))

        if not os.path.exists(quantization_dir):
            os.makedirs(quantization_dir)
        np.save(quantization_path, centers)

        quantization.end_time = timezone.now()
        quantization.save()

        task.quantization_status = 10
        task.save()

    except Exception as e:
        task.quantization_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))

    print('[Quantization] Cluster centers calcluated. Start generate new image.')
    # generate new image
    generation = Generation.objects.create(
        task = task,
        quantization = quantization,
        start_time = timezone.now()
    )

    try:
        generation_dir = os.path.join('workspace', 'generation', str(generation.id))

        if not os.path.exists(generation_dir):
            os.makedirs(generation_dir)
        generation_path = os.path.join('workspace', 'generation', str(generation.id),'result.png')

        # Generate new Image
        print("[Quantization] Generating new image.")
        predictions = model.transform(data_df)
        cluster_indices = predictions.select("prediction").rdd.flatMap(lambda x: x).collect()
        new_image = np.array([centers[i] for i in cluster_indices])
        reshaped_array = new_image.reshape(task.image_id.height, task.image_id.width, 3)
        print("[Quantization] Saving new image")
        
        process = multiprocessing.Process(target=save_image_safely, args=(reshaped_array, generation_path))
        process.start()

        generation.result_image_path = generation_path
        generation.end_time = timezone.now()
        generation.save()

        task.generation_id = generation
        task.generation_status = 10
        task.save()
        print("[Quantization] Kmeans Finished.")
        spark.stop()
        
    except Exception as e:
        task.generation_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))

def bisecting_kmeans(task, quantization, path, k, maxIter, minDivisibleClusterSize, distanceMeasure):
    print("[Quantization] Start Bisecting K-Means")
    # Step 1: train model and generate cluster centers.
    try:
        spark = SparkSession.builder.appName("BisectingKMeans").getOrCreate()
        image = plt.imread(path)  # (1154, 802, 4)
        
        # generate spark data frame
        if image.shape[2] == 4:
            image = image[:, :, :3]
        image = image.reshape(-1, 3)
        data_df = spark.createDataFrame(image.tolist(), ["feature1", "feature2", "feature3"])
        assembler = VectorAssembler(inputCols=["feature1", "feature2", "feature3"], outputCol="features")
        data_df = assembler.transform(data_df)

        # generate spark kmeans model
        kmeans = BisectingKMeans().setK(int(k)).setMaxIter(int(maxIter)).setMinDivisibleClusterSize(float(minDivisibleClusterSize)).setDistanceMeasure(str(distanceMeasure))
        model = kmeans.fit(data_df)
        centers = model.clusterCenters()

        quantization_path = quantization.result_file_path
        quantization_dir = os.path.join('workspace', 'quantization', str(quantization.id))

        if not os.path.exists(quantization_dir):
            os.makedirs(quantization_dir)
        np.save(quantization_path, centers)

        quantization.end_time = timezone.now()
        quantization.save()

        task.quantization_status = 10
        task.save()

    except Exception as e:
        task.quantization_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))
    
    # Step 2: Generate new image using trained model.
    print('[Quantization] Cluster centers calcluated. Start generate new image.')
    # generate new image
    generation = Generation.objects.create(
        task = task,
        quantization = quantization,
        start_time = timezone.now()
    )

    try:
        generation_dir = os.path.join('workspace', 'generation', str(generation.id))

        if not os.path.exists(generation_dir):
            os.makedirs(generation_dir)
        generation_path = os.path.join('workspace', 'generation', str(generation.id),'result.png')

        # Generate new Image
        print("[Quantization] Generating new image")
        predictions = model.transform(data_df)
        cluster_indices = predictions.select("prediction").rdd.flatMap(lambda x: x).collect()
        new_image = np.array([centers[i] for i in cluster_indices])
        reshaped_array = new_image.reshape(task.image_id.height, task.image_id.width, 3)
        
        process = multiprocessing.Process(target=save_image_safely, args=(reshaped_array, generation_path))
        process.start()

        generation.result_image_path = generation_path
        generation.end_time = timezone.now()
        generation.save()

        task.generation_id = generation
        task.generation_status = 10
        task.save()
        print("[Quantization] BisectingKMeans Finished.")
        spark.stop()
        
    except Exception as e:
        # set gene
        task.generation_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))

def gaussian_mixture(task, quantization, path, k, maxIter, tol, aggregationDepth):
    print("[Quantization] Start Gaussian Mixture")
    print(f"[Quantization] Params: maxIter: {maxIter} tol: {tol} aggregationDepth: {aggregationDepth}")
    # Step 1: train model and generate cluster centers.
    try:
        spark = SparkSession.builder.appName("GaussianMixture").getOrCreate()
        image = plt.imread(path)
        
        # generate spark data frame
        if image.shape[2] == 4:
            image = image[:, :, :3]
        image = image.reshape(-1, 3)
        data_df = spark.createDataFrame(image.tolist(), ["feature1", "feature2", "feature3"])
        assembler = VectorAssembler(inputCols=["feature1", "feature2", "feature3"], outputCol="features")
        data_df = assembler.transform(data_df)

        # generate spark kmeans model
        gmm = GaussianMixture().setK(int(k)).setMaxIter(int(maxIter)).setTol(float(tol)).setAggregationDepth(int(aggregationDepth))
        model = gmm.fit(data_df)
        centers_df = model.gaussiansDF
        centers_array = np.array(centers_df.select("mean").collect()).reshape(int(k),3)

        quantization_path = quantization.result_file_path
        quantization_dir = os.path.join('workspace', 'quantization', str(quantization.id))

        if not os.path.exists(quantization_dir):
            os.makedirs(quantization_dir)
        np.save(quantization_path, centers_array)

        quantization.end_time = timezone.now()
        quantization.save()

        
        task.quantization_status = 10
        task.save()

    except Exception as e:
        task.quantization_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))
    
    # Step 2: Generate new image using trained model.
    print('[Quantization] Cluster centers calcluated. Start generate new image.')
    # generate new image
    generation = Generation.objects.create(
        task = task,
        quantization = quantization,
        start_time = timezone.now()
    )

    try:
        generation_dir = os.path.join('workspace', 'generation', str(generation.id))

        if not os.path.exists(generation_dir):
            os.makedirs(generation_dir)
        generation_path = os.path.join('workspace', 'generation', str(generation.id),'result.png')

        # Generate new Image
        print("[Quantization] Generating new image.")
        predictions = model.transform(data_df)
        cluster_indices = predictions.select("prediction").rdd.flatMap(lambda x: x).collect()
        new_image = np.array([centers_array[i] for i in cluster_indices])
        reshaped_array = new_image.reshape(task.image_id.height, task.image_id.width, 3)
        
        process = multiprocessing.Process(target=save_image_safely, args=(reshaped_array, generation_path))
        process.start()

        generation.result_image_path = generation_path
        generation.end_time = timezone.now()
        generation.save()

        
        task.generation_id = generation
        task.generation_status = 10
        task.save()
        print("[Quantization] Gaussian Mixture Finished.")
        spark.stop()
        
    except Exception as e:
        # set gene
        task.generation_status = -1
        task.save()
        print("[Quantization] Failed! Error: "+str(e))

class QuantizationViewSet(viewsets.ViewSet):
        
    def execute_quantization(self, request):
        try:
            # retrieve attributes
            task_id = request.data.get('task_id')
            method = request.data.get('method')
            k = request.data.get('k')
            if not all([task_id,method,k]):
                return JsonResponse(JsonResponse.MISSING_PARAMETERS)
            
            # retrieve related task
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return JsonResponse(JsonResponse.TASK_NOT_EXISTS)
            
            # retrieve status
            if task.image_upload_status != 10:
                return JsonResponse(JsonResponse.IMAGE_NOT_UPLOADED)
            
            image = task.image_id

            path = image.image_path

            if method in ['kmeans', 'KMEANS', 'k-Means', 'kMeans', 'kMEANS']:
                # arguments for kmeans
                maxIter = request.data.get('arg1')
                if maxIter is None or maxIter == '':
                    maxIter = 3
                tol = request.data.get('arg2')
                if tol is None or tol == '':
                    tol = 0.0001
                initSteps = request.data.get('arg3')
                if initSteps is None or initSteps == '':
                    initSteps = 2
                distanceMeasure = request.data.get('arg4')
                if distanceMeasure is None or distanceMeasure == '':
                    distanceMeasure = "euclidean"  
                             
                quantization = Quantization.objects.create(
                    task = task,
                    start_time = timezone.now(),
                    k=k,
                    arg1=maxIter,
                    arg2=tol,
                    arg3=initSteps,
                    arg4=distanceMeasure,
                    method = 'kMeans')
                result_file_path = os.path.join('workspace', 'quantization', str(quantization.id), 'quantization.npy')
                quantization.result_file_path = result_file_path
                quantization.save()
                process = multiprocessing.Process(target=kmeans, args=(task, quantization, path, k, maxIter, tol, initSteps, distanceMeasure))
                process.start()

                task.quantization_id = quantization
                task.quantization_status = 1
                task.save()
                serializer = QuantizationSerializer(quantization)
                return JsonResponse(JsonResponse.SUCCESS,serializer.data)
            elif method in ['BisectingKMeans','bisectingkmeans','bkmeans','bKMeans']:
                                # arguments for kmeans
                maxIter = request.data.get('arg1')
                if maxIter is None or maxIter == '':
                    maxIter = 3
                minDivisibleClusterSize = request.data.get('arg2')
                if minDivisibleClusterSize is None or minDivisibleClusterSize == '':
                    minDivisibleClusterSize = 1
                distanceMeasure = request.data.get('arg4')
                if distanceMeasure is None or distanceMeasure == '':
                    distanceMeasure = "euclidean"  
                             
                quantization = Quantization.objects.create(
                    task = task,
                    start_time = timezone.now(),
                    k=k,
                    arg1=maxIter,
                    arg2=minDivisibleClusterSize,
                    arg4=distanceMeasure,
                    method = 'BisectingKMeans')
                result_file_path = os.path.join('workspace', 'quantization', str(quantization.id), 'quantization.npy')
                quantization.result_file_path = result_file_path
                quantization.save()
                process = multiprocessing.Process(target=bisecting_kmeans, args=(task, quantization, path, k, maxIter, minDivisibleClusterSize, distanceMeasure))
                process.start()

                task.quantization_id = quantization
                task.quantization_status = 1
                task.save()
                serializer = QuantizationSerializer(quantization)
                return JsonResponse(JsonResponse.SUCCESS,serializer.data)
            elif method in ['Gaussian Mixture', 'GaussianMixture', 'gaussian-mixture', 'gaussianmixture', 'gm','gaussianMixture','gMixture','gaussian']:
                # arguments for kmeans
                maxIter = request.data.get('arg1')
                if maxIter is None or maxIter == '':
                    maxIter = 3
                tol = request.data.get('arg2')
                if tol is None or tol == '':
                    tol = 0.0001
                aggregationDepth = request.data.get('arg3')
                if aggregationDepth is None or aggregationDepth == '':
                    aggregationDepth = 2
                             
                quantization = Quantization.objects.create(
                    task = task,
                    start_time = timezone.now(),
                    k=k,
                    arg1=maxIter,
                    arg2=tol,
                    arg3=aggregationDepth,
                    method='GaussianMixture')
                result_file_path = os.path.join('workspace', 'quantization', str(quantization.id), 'quantization.npy')
                quantization.result_file_path = result_file_path
                quantization.save()
                process = multiprocessing.Process(target=gaussian_mixture, args=(task, quantization, path, k, maxIter, tol, aggregationDepth))
                process.start()

                task.quantization_id = quantization
                task.quantization_status = 1
                task.save()
                serializer = QuantizationSerializer(quantization)
                return JsonResponse(JsonResponse.SUCCESS,serializer.data)
            else:
                return JsonResponse(JsonResponse.INAVLID_METHOD)
            
        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))
        
    def retrieve(self, request):
        try:
            pk = request.data.get('quantization_id')

            # empty id
            if not pk:
                return JsonResponse(JsonResponse.EMPTY_ID)

            quantization = Quantization.objects.get(id = pk)
            # wrong id
            if not quantization:
                return JsonResponse(JsonResponse.TASK_NOT_EXISTS)
            result_file_path = quantization.result_file_path
            loaded_colors = np.load(result_file_path)

            colors_list = loaded_colors.tolist()
            serializer = QuantizationSerializer(quantization)

            response_data = {
                'quantization_obj': serializer.data,
                'colors_list': colors_list,
            }

            return JsonResponse(JsonResponse.SUCCESS, response_data)

        except Exception as e:
            return JsonResponse(JsonResponse.INTERNAL_SERVER_ERROR, str(e))