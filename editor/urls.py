"""
URL configuration for pynku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
       path('editor',views.editor_index,name='editor'), 
       path('get_table',views.get_table,name='get_table'),
       path('get_model',views.get_model,name='get_model'),
       path('get_view',views.get_view,name='get_view'),
       path('get_js_view',views.get_js_view,name='get_js_view'),  
       path('get_form',views.get_form,name='get_form'),            
      
] 

