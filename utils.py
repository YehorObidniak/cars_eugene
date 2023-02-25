import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_project.settings")
django.setup()

from django.db import transaction
from main.models import DubicarsCar, DubizzleCar, YallamotorCar, Car_any
import json
from time import time

def add_to_database_dubicars():
    DubicarsCar.objects.all().delete()
    data = json.load(open("dubicars.json", 'r', encoding='utf-8'))
    for info in data:
            if str(info) == "Error" or info == None:
                print(info)
                continue
            car = DubicarsCar(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(''.join(c for c in info['price'] if c.isdigit())),kms=int(''.join(c for c in info['kms'] if c.isdigit())), phone=info['phone'], location=info['location'], regSpecs=info['regSpecs'], year=info['modelDate'], activeListings=info['activeListings'])
            car.save()

def add_to_database_dubizzle():
    DubizzleCar.objects.all().delete()
    data = json.load(open("dubizzle.json", 'r', encoding='utf-8'))
    for info in data:
        if str(info) == "Error" or info == None:
            print(info)
            continue

        price = ''
        try:
            for c in info['price']:
                if c == '.':
                    break
                price = price + c
            
            kms = ''
            for c in info['kilometers']:
                if c.isdigit():
                    kms = kms + c
            try:
                kms = int(kms)
            except:
                kms = 0
        except:
            price = 0
        
        if info['photo'] == None:
            car = DubizzleCar(url=info['url'], make=info['make'], model=info['model'], color=info['color'], photo='no photo', price=int(price),kilometers=kms, posted=info['posted'], active_listings_count=info['active_listings_count'], reg_specs=info['reg_specs'],location=info['location'], year=info['year'])
            continue
        car = DubizzleCar(url=info['url'], make=info['make'], model=info['model'], color=info['color'], photo=info['photo'], price=int(price),kilometers=kms, posted=info['posted'], active_listings_count=info['active_listings_count'], reg_specs=info['reg_specs'],location=info['location'], year=info['year'])
        car.save()

def add_to_database_yallamotor():
    YallamotorCar.objects.all().delete()
    cars = []      
    data = json.load(open("yallamotors.json", 'r', encoding='utf-8'))                                                                                                                    
    for info in data:                                                                                                    
        if str(info) == "Error" or info == None:
            print(info)
            continue
        car = YallamotorCar(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(info['price']),kms=int(''.join(c for c in info['kms'] if c.isdigit())), contact=info['contact'], location=info['location'], regSpecs=info['regSpecs'], year=info['year'], activeListings=info['activeListings'])
        cars.append(car)
        car.save()

class DataBaseManager:
    @transaction.atomic
    def __add_yallamor():
        Car_any.objects.all().filter(site="Yallamotor").delete()
        with transaction.atomic():
            data = json.load(open("yallamotors.json", 'r', encoding='utf-8'))                                                                                                                    
            for info in data:                                                                                                    
                if str(info) == "Error" or info == None:
                    print(info)
                    continue
                car = Car_any(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(info['price']), kms=int(''.join(c for c in info['kms'] if c.isdigit())), contact=info['contact'], location=info['location'], regSpecs=info['regSpecs'], year=info['year'], activeListings=info['activeListings'], posted=time(), site="Yallamotor")
                car.save()

    @transaction.atomic
    def __add_dubicars():
        Car_any.objects.all().filter(site="Dubicars").delete()
        data = json.load(open("dubicars.json", 'r', encoding='utf-8'))
        for info in data:
                if str(info) == "Error" or info == None:
                    print(info)
                    continue
                car = Car_any(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(''.join(c for c in info['price'] if c.isdigit())),kms=int(''.join(c for c in info['kms'] if c.isdigit())), contact=info['phone'], location=info['location'], regSpecs=info['regSpecs'], year=info['modelDate'], activeListings=info['activeListings'], posted=time(), site="Dubicars")
                car.save()
                print("OK")

    @transaction.atomic
    def __add_dubizzle():
        Car_any.objects.all().filter(site="Dubizzle").delete()
        data = json.load(open("dubizzle.json", 'r', encoding='utf-8'))
        for info in data:
            if str(info) == "Error" or info == None:
                print(info)
                continue

            price = ''
            try:
                for c in info['price']:
                    if c == '.':
                        break
                    price = price + c
                
                kms = ''
                for c in info['kilometers']:
                    if c.isdigit():
                        kms = kms + c
                try:
                    kms = int(kms)
                except:
                    kms = 0
            except:
                price = 0
            
            if info['photo'] == None:
                car = Car_any(url=info['url'], brand=info['make'], model=info['model'], color=info['color'], photo='no photo', price=int(price), kms=kms, posted=info['posted'], activeListings=info['active_listings_count'], regSpecs=info['reg_specs'],location=info['location'], year=info['year'], contact="", site="Dubizzle")
                continue
            car = Car_any(url=info['url'], brand=info['make'], model=info['model'], color=info['color'], photo=info['photo'], price=int(price), kms=kms, posted=info['posted'], activeListings=info['active_listings_count'], regSpecs=info['reg_specs'],location=info['location'], year=info['year'], contact="", site="Dubizzle")
            car.save()
            print("OK")

    __add_methods = {"Yallamotor":__add_yallamor, "Dubicars":__add_dubicars, "Dubizzle":__add_dubizzle}

    def add_car(self, site:str):
        try:
            self.__add_methods[site]()
        except Exception as e:
            raise e
            print("incorrect site name")

# add_to_database_dubizzle()
# add_to_database_yallamotor()
# add_to_database_dubicars()
db_manager = DataBaseManager()
# db_manager.add_car("Dubicars")
# db_manager.add_car("Yallamotor")
# db_manager.add_car("Dubizzle")