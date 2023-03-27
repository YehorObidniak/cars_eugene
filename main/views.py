from django.shortcuts import render
from django.http import JsonResponse
from main.models import Car_any
from .filters import CarFilter
from django_user_agents.utils import get_user_agent
from django_sse.views import BaseSseView
from django.db.models import Q
from time import sleep

# Create your views here.
def index(request):
    user_agent = get_user_agent(request)
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())

    if user_agent.is_mobile:
        context = {
                'filter':carFilter.form,
                'dubicarsFilterQs':carFilter.qs.filter(site="Dubicars")[0:50],
            }

        return render(request, 'main/mobile/dubicars.html', context)

    context = {
            'filter':carFilter.form,
            'dubicarsFilterQs':carFilter.qs.filter(site="Dubicars")[0:50],
            'dubizzleFilterQs':carFilter.qs.filter(site="Dubizzle")[0:50],
            'yallamotorFilterQs':carFilter.qs.filter(site="Yallamotor")[0:50],
        }

    return render(request, 'main/desktop/index.html', context)

def dubicars(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubicars").all())

    context = {
        'filter':carFilter.form,
        'dubicarsFilterQs':carFilter.qs[0:50],
    }

    return render(request, 'main/mobile/dubicars.html', context)

def dubizzle(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubizzle").all())

    context = {
        'filter':carFilter.form,
        'dubizzleFilterQs':carFilter.qs[0:50],
    }

    return render(request, 'main/mobile/dubizzle.html', context)

def yallamotor(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Yallamotor").all())

    context = {
        'filter':carFilter.form,
        'yallamotorFilterQs':carFilter.qs[0:50],
    }

    return render(request, 'main/mobile/yallamotor.html', context)

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

class SendSignalView(BaseSseView):
    def iterator(self):
        print(Car_any.objects.filter(Q(listing_type='sale') | Q(listing_type='new')).exists())
        if Car_any.objects.filter(Q(listing_type='sale') | Q(listing_type='new')).exists():
            print('OK')
        self.sse.add_message(event='message', text='run_method')
        yield

def load_new(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all())
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubicars'))
    post_obj_dz = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubizzle'))
    post_obj_yl = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Yallamotor'))

    db_items = int(request.GET.get('db_total'))
    dz_items = int(request.GET.get('dz_total'))
    yl_items = int(request.GET.get('yl_total'))
    print(db_items, dz_items, yl_items)
    data = {
    'new_dubicars':post_obj_db,
    'new_dubizzle':post_obj_dz,
    'new_yallamotor':post_obj_yl,
    }
    return JsonResponse(data=data)