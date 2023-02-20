from main.models import DubicarsCar, DubizzleCar, YallamotorCar
import json

def add_to_database_dubicars():
    DubicarsCar.objects.all().delete()
    cars = []
    data = json.load(open("dubicars.json", 'r', encoding='utf-8'))
    for info in data:
            if str(info) == "Error" or info == None:
                print(info)
                continue
            car = DubicarsCar(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(''.join(c for c in info['price'] if c.isdigit())),kms=int(''.join(c for c in info['kms'] if c.isdigit())), phone=info['phone'])
            cars.append(car)
            car.save()

def add_to_database_dubizzle():
    DubizzleCar.objects.all().delete()
    cars = []
    data = json.load(open("dubizzle.json", 'r', encoding='utf-8'))
    for info in data:
        if str(info) == "Error" or info == None:
            print(info)
            continue
        
        price = ''
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
            
        
        if info['photo'] == None:
            car = DubizzleCar(url=info['url'], make=info['make'], model=info['model'], color=info['color'], photo='no photo', price=int(price),kilometers=kms, posted=info['posted'], active_listings_count=info['active_listings_count'], reg_specs=info['reg_specs'],location=info['location'])
            continue
        car = DubizzleCar(url=info['url'], make=info['make'], model=info['model'], color=info['color'], photo=info['photo'], price=int(price),kilometers=kms, posted=info['posted'], active_listings_count=info['active_listings_count'], reg_specs=info['reg_specs'],location=info['location'])
        cars.append(car)
        car.save()

def add_to_database_yallamotor():
    YallamotorCar.objects.all().delete()
    cars = []
    data = json.load(open("yallamotors.json", 'r', encoding='utf-8'))
    for info in data:
        if str(info) == "Error" or info == None:
            print(info)
            continue
        car = YallamotorCar(url=info['url'], brand=info['brand'], model=info['model'], color=info['color'], photo=info['photo'], price=int(info['price']),kms=int(''.join(c for c in info['kms'] if c.isdigit())), contact=info['contact'])
        cars.append(car)
        car.save()
    
# add_to_database_dubizzle()
# add_to_database_yallamotor()
# add_to_database_dubicars()