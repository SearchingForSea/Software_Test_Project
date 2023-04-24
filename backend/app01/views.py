from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.utils import json
from .models import test

# Create your views here.


@require_http_methods(['GET'])
def show_res(request):
    return HttpResponse("no")

