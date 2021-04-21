import random
import time
from flask import Flask, request
import socketio
import requests

def my_location():
    loc = random.randint(-100,100)
    return loc

if __name__ == '__main__':

    riders = [['Autoshi',1],['Moon',2],['Badhon',3],['Rifat',4],['Roky',5],['Al-amin',6],['Rukon',7],
              ['Ramjan',8],['Sihan',9],['Mamun',10],['Munni',11],['Bristy',12]]

    drivers = [['Jakaria',1],['Minal',2],['Pranto',3],['Nadim',4],['Rakib',5],['Rafat',6],['Monju',7],['Shanto',8]]

    cars = ['DS-98379','DS-12344','DS-45129','DS-31179','DS-41370','DS-18479','LL-124379','DL-12566',8]

    socket = socketio.Client()
    socket.connect('http://127.0.0.1:5000', namespaces=['/confirmation'])

    @socket.on('message', namespace='/confirmation')
    def notify(data):
        print(f"Driver {data['driver']} is coming to pick up rider {data['rider']}, Ride fair:{data['fair']}")
        rating = random.randint(1, 5)
        
        print("Rating : ",rating)

        print(f"{data['rider']} gave driver {data['driver']} a rating of {rating}/5!")
        rate_info = {
            "rider_name": data['rider'],
            "r_id": data['rider_id'],
            "driver_name": data['driver'],
            "d_id": data['driver_id'],
            "rating": rating
        }
        requests.post("http://127.0.0.1:5000/rating", json=rate_info)


    while True:
        r = random.choice(riders)
        d = random.choice(drivers)
        rider = {
            "name": r[0],
            "id": r[1],
            "coordinates": [my_location(),my_location()],
            "destination": [my_location(),my_location()]
        }
        driver = {
            "name": d[0],
            "id": d[1],
            "coordinates": [my_location(), my_location()],
            "car_number": random.choice(cars)
        }

        requests.post("http://127.0.0.1:5000/rider", json= rider)
        print(rider['name'], "is looking for a ride")
        requests.post("http://127.0.0.1:5000/driver", json= driver)
        print(driver['name'], "is looking for a trip")
        time.sleep(2)