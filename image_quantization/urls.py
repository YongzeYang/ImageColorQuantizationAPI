"""
URL configuration for image_quantization project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers

from image.views import ImageViewSet
from quantization.views import QuantizationViewSet
from task.views import TaskViewSet
from generation.views import GenerationViewSet
from rest_framework.authtoken import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('task/create/', TaskViewSet.as_view({'post': 'create',
                                              'get':'create'})),
    path('task/retrieve/', TaskViewSet.as_view({'post': 'retrieve',
                                                'get': 'retrieve'})),
    path('task/list/', TaskViewSet.as_view({'post': 'list',
                                            'get': 'list'})),
    path('image/upload/', ImageViewSet.as_view({'post':'upload_image'})),
    path('image/retrieve/', ImageViewSet.as_view({'get':'retrieve',
                                                  'post':'retrieve'})),
    path('image/download/', ImageViewSet.as_view({'get':'download',
                                                  'post':'download'})),
    
    path('quantization/execute/', QuantizationViewSet.as_view({'post':'execute_quantization'})),
    path('quantization/retrieve/', QuantizationViewSet.as_view({'get':'retrieve',
                                                  'post':'retrieve'})),
    path('generation/retrieve/', GenerationViewSet.as_view({'get':'retrieve',
                                                  'post':'retrieve'})),
    path('generation/download/', GenerationViewSet.as_view({'get':'download',
                                                  'post':'download'})),                                      
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}