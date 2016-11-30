from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # Routes all 'http://<website>/api/' requests to the index function in api/views.py
]