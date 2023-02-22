from django.shortcuts import render
from django.http import JsonResponse
from main.models import DubicarsCar, DubizzleCar, YallamotorCar
from .filters import DubicarsCarFilter, DubizzleCarFilter, YallamotorCarFilter

# Create your views here.
def index(request):
    dubicarsFilter = DubicarsCarFilter(request.GET, queryset=DubicarsCar.objects.all(), prefix='dubicars')
    dubizzleFilter = DubizzleCarFilter(request.GET, queryset=DubizzleCar.objects.all(), prefix='dubizzle')
    yallamotorFilter = YallamotorCarFilter(request.GET, queryset=YallamotorCar.objects.all(), prefix='yallamotor')

    context = {
        'dubicarsFilter':dubicarsFilter.form,
        'dubizzleFilter':dubizzleFilter.form,
        'yallamotorFilter':yallamotorFilter.form,
        'dubicarsFilterQs':dubicarsFilter.qs[0:50],
        'dubizzleFilterQs':dubizzleFilter.qs[0:50],
        'yallamotorFilterQs':yallamotorFilter.qs[0:50],
    }

    return render(request, 'main/index.html', context)

def load_more_dubicars(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    dubicarsFilter = DubicarsCarFilter(request.GET, queryset=DubicarsCar.objects.all(), prefix='dubicars')
    post_obj = list(dubicarsFilter.qs.values()[total_item:total_item+limit])
    data = {
        'dubicars':post_obj
    }
    return JsonResponse(data=data)

def load_more_dubizzle(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    dubizzleFilter = DubizzleCarFilter(request.GET, queryset=DubizzleCar.objects.all(), prefix='dubizzle')
    post_obj = list(dubizzleFilter.qs.values()[total_item:total_item+limit])
    data = {
        'dubizzle':post_obj
    }
    return JsonResponse(data=data)

def load_more_yallamotor(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    yallamotorFilter = YallamotorCarFilter(request.GET, queryset=YallamotorCar.objects.all(), prefix='yallamotor')
    post_obj = list(yallamotorFilter.qs.values()[total_item:total_item+limit])
    data = {
        'yallamotor':post_obj
    }
    return JsonResponse(data=data)