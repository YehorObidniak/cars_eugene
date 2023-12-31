"""cars_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from main.views import index, load_more_dubicars, load_more_dubizzle, load_more_yallamotor, dubicars, dubizzle, yallamotor, SendSignalView, load_new, load_more_new_dubicars, load_more_new_dubizzle, load_more_new_yallamotor, load_new_dubicars, load_new_dubizzle, load_new_yallamotor, login, custom_logout, load_more, load_new_all, load_more_new_all

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('dubicars/', dubicars, name='dubicars'),
    path('dubizzle/', dubizzle, name='dubizzle'),
    path('yallamotor/', yallamotor, name='yallamotor'),
    path('load_dubicars/', load_more_dubicars, name='load_dubicars'),
    path('load_dubizzle/', load_more_dubizzle, name='load_dubizzle'),
    path('load_yallamotor/', load_more_yallamotor, name='load_yallamotor'),
    path('load_new/', load_new, name='load_new'),
    path('signal/', SendSignalView.as_view(), name='send_signal'),
    path('load_new_dubicars/', load_new_dubicars, name='load_new_dubicars'),
    path('load_new_dubizzle/', load_new_dubizzle, name='load_new_dubizzle'),
    path('load_new_yallamotor/', load_new_yallamotor, name='load_new_yallamotor'),
    path('load_more_new_dubicars/', load_more_new_dubicars, name='load_more_new_dubicars'),
    path('load_more_new_dubizzle/', load_more_new_dubizzle, name='load_more_new_dubizzle'),
    path('load_more_new_yallamotor/', load_more_new_yallamotor, name='load_more_new_yallamotor'),
    path('login/', login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('load_more/', load_more, name='load_more'),
    path('load_new_all/', load_new_all, name='load_new_all'),
    path('load_more_new_all/', load_more_new_all, name='load_more_new_all')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

