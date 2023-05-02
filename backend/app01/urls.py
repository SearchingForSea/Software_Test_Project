from django.conf.urls import url
from . import views

urlpatterns = [
    url('show_res', views.get_info),
    url('basic_info', views.basic_info)
]