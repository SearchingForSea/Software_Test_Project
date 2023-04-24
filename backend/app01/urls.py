from django.conf.urls import url
from . import views

urlpatterns = [
    url('show_res', views.show_res),
]