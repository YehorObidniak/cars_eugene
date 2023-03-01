import django_filters
from .models import Car_any, Brands, regSpecs
from django_filters.widgets import RangeWidget
from django.forms import TextInput, Select
from django.db.models import F, Q

#Filters for car class 
class CarFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(widget=RangeWidget(attrs={'class':'inp_price'}))
    brand = django_filters.ChoiceFilter(lookup_expr='contains', choices=Brands.objects.order_by(F('name').asc()).values_list('name', 'name'), widget=Select(attrs={'class':'inp'}))
    model = django_filters.CharFilter(lookup_expr='contains', widget=TextInput(attrs={'class':'inp', 'placeholder':'Type model...'}))
    kms = django_filters.RangeFilter(widget=RangeWidget(attrs={'class':'inp_kms'}))
    location = django_filters.CharFilter(lookup_expr='contains', widget=TextInput(attrs={'class':'inp', 'placeholder':'Type location...'}))
    year = django_filters.RangeFilter(widget=RangeWidget(attrs={'class':'inp_year'}))
    regSpecs = django_filters.ChoiceFilter(method='filter_exclude_spec', choices=regSpecs.objects.order_by('name').values_list('name', 'name'), widget=Select(attrs={'class':'inp'}))

    class Meta:
        model = Car_any
        fields = ({'price', 'brand', 'model', 'kms', 'location', 'regSpecs'})

    def filter_exclude_spec(self, queryset, name, value):
        if value != 'GCC':
            return queryset.filter(Q(regSpecs__contains=value) | Q(regSpecs__contains='import'))
        return queryset.filter(regSpecs__contains='GCC')