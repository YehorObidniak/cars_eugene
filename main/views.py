from django.shortcuts import render
from django.http import JsonResponse
from main.models import Car_any
from .filters import CarFilter

# Create your views here.
def index(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())

    context = {
        'filter':carFilter.form,
        'dubicarsFilterQs':carFilter.qs.filter(site="Dubicars")[0:50],
        'dubizzleFilterQs':carFilter.qs.filter(site="Dubizzle")[0:50],
        'yallamotorFilterQs':carFilter.qs.filter(site="Yallamotor")[0:50],
    }

    return render(request, 'main/index.html', context)

def load_more_dubicars(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())
    post_obj = list(carFilter.qs.values().filter(site="Dubicars")[total_item:total_item+limit])
    data = {
        'dubicars':post_obj
    }
    return JsonResponse(data=data)

def load_more_dubizzle(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())
    post_obj = list(carFilter.qs.values().filter(site="Dubizzle")[total_item:total_item+limit])
    data = {
        'dubizzle':post_obj
    }
    return JsonResponse(data=data)

def load_more_yallamotor(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())
    post_obj = list(carFilter.qs.values().filter(site="Yallamotor")[total_item:total_item+limit])
    data = {
        'yallamotor':post_obj
    }
    return JsonResponse(data=data)