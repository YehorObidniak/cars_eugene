from django.shortcuts import render, redirect
from django.http import JsonResponse
from main.models import Car_any, Sellers
from .filters import CarFilter
from django_user_agents.utils import get_user_agent
from django_sse.views import BaseSseView
from django.db.models import Q, IntegerField
from django.db.models.functions import Floor, Cast
from time import time as tm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as log, logout

# Create your views here.

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            log(request, user)            
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

@login_required(login_url='login')
def index(request):
    user_agent = get_user_agent(request)
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(activeForSite=True))
    regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubicars').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
    

    if user_agent.is_mobile:
        context = {
                'filter':carFilter.form,
                'newDubicars':post_obj_db[0:50], 
                'dubicarsFilterQs':regCars.filter(site="Dubicars")[0:50],
            }

        return render(request, 'main/mobile/dubicars.html', context)
    
    post_obj_dz = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubizzle').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
    post_obj_yl = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Yallamotor').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
    context = {
            'filter':carFilter.form,
            'dubicarsFilterQs':regCars.filter(site="Dubicars")[0:50],
            'dubizzleFilterQs':regCars.filter(site="Dubizzle")[0:50],
            'yallamotorFilterQs':regCars.filter(site="Yallamotor")[0:50],
            'newDubicars':post_obj_db[0:50], 
            'newDubizzle':post_obj_dz[0:50],
            'newYallamotor':post_obj_yl[0:50],
        }

    return render(request, 'main/desktop/index.html', context)

@login_required(login_url='login')
def dubicars(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubicars").filter(activeForSite=True).all())
    regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubicars').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

    context = {
        'filter':carFilter.form,
        'dubicarsFilterQs':regCars[0:50],
        'newDubicars':post_obj_db[0:50], 
    }

    return render(request, 'main/mobile/dubicars.html', context)

@login_required(login_url='login')
def dubizzle(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubizzle").filter(activeForSite=True).all())
    regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubizzle').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

    context = {
        'filter':carFilter.form,
        'dubizzleFilterQs':regCars[0:50],
        'newDubizzle':post_obj_db[0:50], 
    }

    return render(request, 'main/mobile/dubizzle.html', context)

@login_required(login_url='login')
def yallamotor(request):
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Yallamotor").filter(activeForSite=True).all())
    regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Yallamotor').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

    context = {
        'filter':carFilter.form,
        'yallamotorFilterQs':regCars[0:50],
        'newYallamotor':post_obj_db[0:50], 
    }

    return render(request, 'main/mobile/yallamotor.html', context)

def load_more_dubicars(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
    post_obj = list(carFilter.qs.values().filter(site="Dubicars")[total_item:total_item+limit])
    data = {
        'dubicars':post_obj
    }
    return JsonResponse(data=data)

def load_more_dubizzle(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
    post_obj = list(carFilter.qs.values().filter(site="Dubizzle")[total_item:total_item+limit])
    data = {
        'dubizzle':post_obj
    }
    return JsonResponse(data=data)

def load_more_yallamotor(request):
    total_item = int(request.GET.get('total_item'))
    limit = 30
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
    post_obj = list(carFilter.qs.values().filter(site="Yallamotor")[total_item:total_item+limit])
    data = {
        'yallamotor':post_obj
    } 
    return JsonResponse(data=data)

class SendSignalView(BaseSseView):
    def iterator(self):
        time = int(self.request.GET.get('lastsignal'))
        currTime = int(tm())
        if Car_any.objects.filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(activeForSite=True).filter(post_created_at__gte=time).filter(post_created_at__lt=currTime).exists():
            print('OK')
            self.sse.add_message(event='message', text=f'run_method;{time};{currTime}')
        else:
            self.sse.add_message(event='message', text=f'No new posts;{time};{currTime}')
        yield


def load_new(request):
    time = int(request.GET.get('time'))
    curTime = int(request.GET.get('curTime'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
    post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubicars').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
    post_obj_dz = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubizzle').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
    post_obj_yl = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Yallamotor').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))

    data = {
    'new_dubicars':post_obj_db,
    'new_dubizzle':post_obj_dz,
    'new_yallamotor':post_obj_yl,
    }
    return JsonResponse(data=data)

def load_new_dubicars(request):
    time = int(request.GET.get('time'))
    curTime = int(request.GET.get('curTime'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
    post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubicars').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
    data = {
        'new_dubicars':post_obj
    }
    return JsonResponse(data=data)

def load_new_dubizzle(request):
    time = int(request.GET.get('time'))
    curTime = int(request.GET.get('curTime'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
    post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubizzle').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
    data = {
        'new_dubizzle':post_obj
    }
    return JsonResponse(data=data)

def load_new_yallamotor(request):
    time = int(request.GET.get('time'))
    curTime = int(request.GET.get('curTime'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
    post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Yallamotor').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
    data = {
        'new_yallamotor':post_obj
    }
    return JsonResponse(data=data)

def load_more_new_dubicars(request):
    total = int(request.GET.get('total_item'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Dubicars').filter(activeForSite=True))
    data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
    return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})

def load_more_new_dubizzle(request):
    total = int(request.GET.get('total_item'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Dubizzle').filter(activeForSite=True))
    data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
    print(len(data))
    return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})

def load_more_new_yallamotor(request):
    total = int(request.GET.get('total_item'))
    carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Yallamotor').filter(activeForSite=True))
    data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
    print(len(data))
    return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})


# from django.shortcuts import render
# from django.http import JsonResponse
# from main.models import Car_any, Sellers
# from .filters import CarFilter
# from django_user_agents.utils import get_user_agent
# from django_sse.views import BaseSseView
# from django.db.models import Q, IntegerField
# from django.db.models.functions import Floor, Cast
# from time import time as tm
# from math import floor

# # Create your views here.
# def index(request):
#     user_agent = get_user_agent(request)
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(activeForSite=True))
#     regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
#     post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubicars').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
    

#     if user_agent.is_mobile:
#         context = {
#                 'filter':carFilter.form,
#                 'newDubicars':post_obj_db[0:50], 
#                 'dubicarsFilterQs':regCars.filter(site="Dubicars")[0:50],
#             }

#         return render(request, 'main/mobile/dubicars.html', context)
    
#     post_obj_dz = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubizzle').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
#     post_obj_yl = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Yallamotor').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))
#     context = {
#             'filter':carFilter.form,
#             'dubicarsFilterQs':regCars.filter(site="Dubicars")[0:50],
#             'dubizzleFilterQs':regCars.filter(site="Dubizzle")[0:50],
#             'yallamotorFilterQs':regCars.filter(site="Yallamotor")[0:50],
#             'newDubicars':post_obj_db[0:50], 
#             'newDubizzle':post_obj_dz[0:50],
#             'newYallamotor':post_obj_yl[0:50],
#         }

#     return render(request, 'main/desktop/index.html', context)

# def dubicars(request):
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubicars").filter(activeForSite=True).all())
#     regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
#     post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubicars').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

#     context = {
#         'filter':carFilter.form,
#         'dubicarsFilterQs':regCars[0:50],
#         'newDubicars':post_obj_db[0:50], 
#     }

#     return render(request, 'main/mobile/dubicars.html', context)

# def dubizzle(request):
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Dubizzle").filter(activeForSite=True).all())
#     regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
#     post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Dubizzle').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

#     context = {
#         'filter':carFilter.form,
#         'dubizzleFilterQs':regCars[0:50],
#         'newDubizzle':post_obj_db[0:50], 
#     }

#     return render(request, 'main/mobile/dubizzle.html', context)

# def yallamotor(request):
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(site="Yallamotor").filter(activeForSite=True).all())
#     regCars = carFilter.qs.filter(listing_type='Regular').order_by('-post_created_at')
#     post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='sale') | Q(listing_type='new')).filter(site='Yallamotor').annotate(int_post_created_at=Cast('post_created_at', IntegerField())).order_by('-int_post_created_at'))

#     context = {
#         'filter':carFilter.form,
#         'yallamotorFilterQs':regCars[0:50],
#         'newYallamotor':post_obj_db[0:50], 
#     }

#     return render(request, 'main/mobile/yallamotor.html', context)

# def load_more_dubicars(request):
#     total_item = int(request.GET.get('total_item'))
#     limit = 30
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
#     post_obj = list(carFilter.qs.values().filter(site="Dubicars")[total_item:total_item+limit])
#     data = {
#         'dubicars':post_obj
#     }
#     return JsonResponse(data=data)

# def load_more_dubizzle(request):
#     total_item = int(request.GET.get('total_item'))
#     limit = 30
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
#     post_obj = list(carFilter.qs.values().filter(site="Dubizzle")[total_item:total_item+limit])
#     data = {
#         'dubizzle':post_obj
#     }
#     return JsonResponse(data=data)

# def load_more_yallamotor(request):
#     total_item = int(request.GET.get('total_item'))
#     limit = 30
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(listing_type='Regular').filter(activeForSite=True).order_by('-post_created_at'))
#     post_obj = list(carFilter.qs.values().filter(site="Yallamotor")[total_item:total_item+limit])
#     data = {
#         'yallamotor':post_obj
#     } 
#     return JsonResponse(data=data)

# class SendSignalView(BaseSseView):
#     def iterator(self):
#         time = int(self.request.GET.get('lastsignal'))
#         currTime = int(tm())
#         if Car_any.objects.filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(activeForSite=True).filter(post_created_at__gte=time).filter(post_created_at__lt=currTime).exists():
#             print('OK')
#             self.sse.add_message(event='message', text=f'run_method;{time};{currTime}')
#         else:
#             self.sse.add_message(event='message', text=f'No new posts;{time};{currTime}')
#         yield


# def load_new(request):
#     time = int(request.GET.get('time'))
#     curTime = int(request.GET.get('curTime'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
#     post_obj_db = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubicars').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
#     post_obj_dz = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubizzle').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
#     post_obj_yl = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Yallamotor').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))

#     data = {
#     'new_dubicars':post_obj_db,
#     'new_dubizzle':post_obj_dz,
#     'new_yallamotor':post_obj_yl,
#     }
#     return JsonResponse(data=data)

# def load_new_dubicars(request):
#     time = int(request.GET.get('time'))
#     curTime = int(request.GET.get('curTime'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
#     post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubicars').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
#     data = {
#         'new_dubicars':post_obj
#     }
#     return JsonResponse(data=data)

# def load_new_dubizzle(request):
#     time = int(request.GET.get('time'))
#     curTime = int(request.GET.get('curTime'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
#     post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Dubizzle').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
#     data = {
#         'new_dubizzle':post_obj
#     }
#     return JsonResponse(data=data)

# def load_new_yallamotor(request):
#     time = int(request.GET.get('time'))
#     curTime = int(request.GET.get('curTime'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.filter(activeForSite=True).all())
#     post_obj = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).filter(site='Yallamotor').filter(post_created_at__gte=time).filter(post_created_at__lt=curTime).order_by('brand'))
#     data = {
#         'new_yallamotor':post_obj
#     }
#     return JsonResponse(data=data)

# def load_more_new_dubicars(request):
#     total = int(request.GET.get('total_item'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Dubicars').filter(activeForSite=True))
#     data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
#     return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})

# def load_more_new_dubizzle(request):
#     total = int(request.GET.get('total_item'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Dubizzle').filter(activeForSite=True))
#     data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
#     print(len(data))
#     return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})

# def load_more_new_yallamotor(request):
#     total = int(request.GET.get('total_item'))
#     carFilter = CarFilter(request.GET, queryset=Car_any.objects.all().filter(site='Yallamotor').filter(activeForSite=True))
#     data = list(carFilter.qs.values().filter(Q(listing_type='Sale') | Q(listing_type='New')).order_by('-post_created_at'))
#     print(len(data))
#     return JsonResponse(data={'data':data[total:total+50], 'all':True if len(data) - total - 50 <= 0 else False})