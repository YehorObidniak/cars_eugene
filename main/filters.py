import django_filters
from .models import DubicarsCar, DubizzleCar, YallamotorCar, Car_any

class DubicarsCarFilter(django_filters.FilterSet):

    class Meta:
        model = DubicarsCar
        fields = {'price':{'range'}, 'brand':{'contains'}, 'kms':{'range'}, 'model':{'contains'}}

class DubizzleCarFilter(django_filters.FilterSet):

    class Meta:
        model = DubizzleCar
        fields = {'price':{'range'}, 'make':{'contains'}, 'kilometers':{'range'}, 'model':{'contains'}, 'reg_specs':{'contains'}}

class YallamotorCarFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(
        lookup_expr="range",
        label="Type min and max"
    )

    class Meta:
        model = YallamotorCar
        fields = {'brand':{'contains'}, 'kms':{'range'}, 'model':{'contains'}}


#Filters for car class 
class CarFilter(django_filters.FilterSet):

    class Meta:
        model = Car_any
        fields = {'price':{'range'}, 'brand':{'contains'}, 'kms':{'range'}, 'model':{'contains'}}