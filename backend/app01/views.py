from django.shortcuts import render
from django.http import HttpResponse
from .models import test
from django.core import serializers

# Create your views here.
def get_info(request):
    return HttpResponse("no")

def basic_info(request):
    if request.method == 'GET':
        # try:
        es_data = test.objects.all()
        return_es_data = serializers.serialize('json', es_data, ensure_ascii=False)
        print(return_es_data)
        return HttpResponse(return_es_data)
        # except:
        #     return HttpResponse('no')