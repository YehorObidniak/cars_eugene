from django.shortcuts import render
from django.http import JsonResponse
from main.models import DubicarsCar, DubizzleCar, YallamotorCar, Car_any
from .filters import DubicarsCarFilter, DubizzleCarFilter, YallamotorCarFilter, CarFilter

# Create your views here.
def index(request):
    # dubicarsFilter = DubicarsCarFilter(request.GET, queryset=DubicarsCar.objects.all(), prefix='dubicars')
    # dubizzleFilter = DubizzleCarFilter(request.GET, queryset=DubizzleCar.objects.all(), prefix='dubizzle')
    # yallamotorFilter = YallamotorCarFilter(request.GET, queryset=YallamotorCar.objects.all(), prefix='yallamotor')

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