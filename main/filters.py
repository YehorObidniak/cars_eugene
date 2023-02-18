import django_filters
from .models import DubicarsCar, DubizzleCar, YallamotorCar

class DubicarsCarFilter(django_filters.FilterSet):

    class Meta:
        model = DubicarsCar
        fields = {'price':{'range'}, 'brand':{'contains'}, 'kms':{'range'}, 'model':{'contains'}}

class DubizzleCarFilter(django_filters.FilterSet):

    class Meta:
        model = DubizzleCar
        fields = {'price':{'range'}, 'make':{'contains'}, 'kilometers':{'range'}, 'model':{'contains'}, 'reg_specs':{'contains'}}

class YallamotorCarFilter(django_filters.FilterSet):

    class Meta:
        model = YallamotorCar
        fields = {'price':{'range'}, 'brand':{'contains'}, 'kms':{'range'}, 'model':{'contains'}}