from django.urls import re_path
from . import views

urlpatterns = [
    re_path('show_res', views.get_info),
    re_path('basic_info', views.basic_info),
    re_path('balancing_node_steps', views.distribute_node),
    re_path('manage_resource', views.manage_resource)
]