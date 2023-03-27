import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cars_project.settings")
django.setup()

from main.models import Car_any, Brands, regSpecs
import json
from time import time
import threading
from queue import Queue
from django.db import connections
from django.db import transaction

class DataBaseManager:

    def add(self, count, data):
        for i in range(count):                                                                                       
            if str(data[i]) == "Error" or data[i] == None:
                print(data[i])
                continue

            car_brand = data[i]['brand'].strip()
            if not Brands.objects.all().filter(name=car_brand).exists():
                brand = Brands(name=car_brand)
                # brand.save()
            
            car_spec = data[i]['regSpecs'].replace('Specs', '').strip()
            if not regSpecs.objects.all().filter(name=car_spec).exists() and car_spec != 'Yes' and car_spec != 'Does not apply':
                spec = regSpecs(name=car_spec)
                # spec.save()

            car = Car_any(
                url=data[i]['url'],
                brand=car_brand, 
                model=data[i]['model'], 
                color=data[i]['color'], 
                photo=data[i]['photo'], 
                price=int(data[i]['price']), 
                kms=int(''.join(c for c in data[i]['kms'] if c.isdigit())), 
                contact=data[i]['contact'], 
                location=data[i]['location'], 
                regSpecs=car_spec, 
                year=data[i]['year'], 
                posted=time(), 
                site="Yallamotor", 
                activeListings=data[i]['activeListings']
                )
            print(i)
            car.save()

    def __add_yallamor(self):
        cars = []
        threads = []
        MAX_WORKERS = 50

        Car_any.objects.all().filter(site="Yallamotor").delete()
        
        data = json.load(open("yallamotors.json", 'r', encoding='utf-8'))       

        count = len(data) // MAX_WORKERS
        for i in range(MAX_WORKERS):
            t = threading.Thread(target=self.add, args=(count, data[i*count:(i+1)*count]))  
            t.start()
            threads.append(t)

        t = threading.Thread(target=self.add, args=(count, data[len(data)-(MAX_WORKERS*count):len(data)-(len(data)-(MAX_WORKERS*count))]))
        t.start()
        threads.append(t)
        print(threads)

        for t in threads:
            t.join()
        
        
        
            
    @transaction.atomic()
    def __add_dubicars():
        Car_any.objects.all().filter(site="Dubicars").delete()

        data = json.load(open("dubicars.json", 'r', encoding='utf-8'))

        j = 0
        for info in data:
                if str(info) == "Error" or info == None:
                    print(info)
                    continue

                car_brand = info['brand'].strip()
                if not Brands.objects.all().filter(name=car_brand).exists():
                    brand = Brands(name=car_brand)
                    brand.save()
                
                car_spec = info['regSpecs'].replace('Specs', '').strip()
                if not regSpecs.objects.all().filter(name=car_spec).exists() and car_spec != 'Yes' and car_spec != 'Does not apply':
                    spec = regSpecs(name=car_spec)
                    spec.save()

                car = Car_any(
                    url=info['url'], 
                    brand=car_brand, 
                    model=info['model'], 
                    color=info['color'], 
                    photo=info['photo'], 
                    price=int(''.join(c for c in info['price'] if c.isdigit())),
                    kms=int(''.join(c for c in info['kms'] if c.isdigit())), 
                    contact=info['phone'], location=info['location'], 
                    regSpecs=car_spec, 
                    year=info['modelDate'], 
                    activeListings=info['activeListings'], 
                    posted=time(), 
                    site="Dubicars"
                    )
                car.save()
                print(j)
                j+=1

    @transaction.atomic
    def __add_dubizzle():
        Car_any.objects.all().filter(site="Dubizzle").delete()
        data = json.load(open("dubizzle.json", 'r', encoding='utf-8'))

        j = 0
        for info in data:
            if str(info) == "Error" or info == None:
                print(info)
                continue
            
            try:
                car_listings = int(info['active_listings_count'])
            except:
                continue
        
            car_brand = info['make'].strip()
            if not Brands.objects.all().filter(name=car_brand).exists():
                brand = Brands(name=car_brand)
                brand.save()
            
            car_spec = info['reg_specs'].replace('Specs', '').strip()
            if not regSpecs.objects.all().filter(name=car_spec).exists() and car_spec != 'Yes' and car_spec != 'Does not apply':
                spec = regSpecs(name=car_spec)
                spec.save()

            if info['photo'] == None:
                car = Car_any(
                    url=info['url'], 
                    brand=car_brand, 
                    model=info['model'], 
                    color=info['color'], 
                    photo='no photo', 
                    price=int(info['price']), 
                    kms=int(info['kilometers']), 
                    posted=info['posted'], 
                    activeListings=info['active_listings_count'], 
                    regSpecs=car_spec,
                    location=info['location'], 
                    year=info['year'], 
                    contact="", 
                    site="Dubizzle"
                    )
                car.save()
                continue

            car = Car_any(
                url=info['url'], 
                brand=car_brand, 
                model=info['model'], 
                color=info['color'], 
                photo=info['photo'], 
                price=int(info['price']), 
                kms=int(info['kilometers']), 
                posted=info['posted'], 
                activeListings=info['active_listings_count'], 
                regSpecs=car_spec,
                location=info['location'], 
                year=info['year'], 
                contact="", 
                site="Dubizzle"
                )
            car.save()
            print(j)
            j+=1

    __add_methods = {"Yallamotor":__add_yallamor, "Dubicars":__add_dubicars, "Dubizzle":__add_dubizzle}

    def add_one_car(self, site:str):
        try:
            self.__add_methods[site](self)
        except Exception as e:
            print("incorrect site name")
            raise e

    def add_cars(self):
        Brands.objects.all().delete()
        regSpecs.objects.all().delete()
        self.__add_methods["Dubicars"]()
        self.__add_methods["Yallamotor"]()
        self.__add_methods["Dubizzle"]()
            
db_manager = DataBaseManager()
db_manager.add_one_car('Yallamotor')
# db_manager.add_cars()
# Car_any.objects.all().delete()

# car = Car_any(
#     url = 'https://dubai.dubizzle.com/motors/used-cars/dodge/charger/2023/2/28/dodge-charger-sxt-2019-2-097---b649a3e858a348fb88e48a630a695919/',
#     brand = 'Mercedes-Benz',
#     model = 'CLS 500',
#     color = 'Grey/Silver',
#     photo = 'https://dbz-images.dubizzle.com/images/2023/02/28/6129c6ee76b2420d87d29b3c9460e7cb-.jpeg?impolicy=legacy&imwidth=480',
#     kms = '130000',
#     contact = 'tel:+971507730011',
#     year = '2002',
#     location = 'Al Ain',
#     regSpecs = 'GCC',
#     activeListings = 1,
#     posted = '1679538423.7717562',
#     site = 'Dubizzle',
#     active = 1,
#     listing_type_changed = 0,
#     price = 14000,
#     listing_type = 'sale'
# )
# car.save()

# upd = Car_any.objects.filter(url = 'https://www.dubicars.com/2002-mercedes-benz-cls-500-552122.html').update(listing_type='new')

# def add(count, data):
#     for i in range(count):
#         if data[i]['model'] == "main.car_any":
#             car = Car_any(
#                 url=data[i]['pk'],
#                 brand=data[i]['fields']['brand'], 
#                 model=data[i]['fields']['model'], 
#                 color=data[i]['fields']['color'], 
#                 photo=data[i]['fields']['photo'], 
#                 price=int(data[i]['fields']['price']), 
#                 kms=int(data[i]['fields']['kms']), 
#                 contact=data[i]['fields']['contact'], 
#                 location=data[i]['fields']['location'], 
#                 regSpecs=data[i]['fields']['regSpecs'], 
#                 year=data[i]['fields']['year'], 
#                 posted=data[i]['fields']['time'], 
#                 site=data[i]['fields']['site'], 
#                 activeListings=data[i]['fields']['activeListings'],
#                 active = data[i]['fields']['active'],
#                 old_price = data[i]['fields']['old_price'],
#                 listing_type = data[i]['fields']['listing_type']
#             )
#             print(i)
#             car.save()

# def json_to_db():
            