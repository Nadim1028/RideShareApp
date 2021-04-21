# from flask import Flask
#
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return "Hi! Nadim"
#
# if __name__=="main":
#     app.run(debug=True)


import json
from datetime import datetime
import math
import flask
import mysql.connector
from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
from flask_apscheduler import APScheduler

avail_riders = []
avail_drivers = []
app = Flask(__name__)
socket = SocketIO(app)

scheduler = APScheduler()
scheduler.init_app(app)


@app.route('/')
def index():
    return "Hi! Nadim"

if __name__=="main":
    app.run(debug=True)


socket.run(app, port=5000)
scheduler.start()


@scheduler.task('interval', id="make_pair", seconds=5, misfire_grace_time=None)
def make_pair():

    def calculate_distance(rider, driver):
        rider_x, rider_y = [int(i) for i in rider['coordinates']]
        driver_x, driver_y = [int(i) for i in driver['coordinates']]
        return math.sqrt(pow(rider_x - driver_x, 2) + pow(rider_y - driver_y, 2))

    for rider in avail_riders:
        distance_min = 10000000000000
        nearest_driver = None
        for driver in avail_drivers:
            distance = calculate_distance(rider, driver)
            if distance_min > distance:
                distance_min = distance
                nearest_driver = driver

        avail_riders.remove(rider)
        avail_drivers.remove(nearest_driver)

        data = {
            "rider": rider['name'],
            "rider_id": rider['id'],
            "driver": nearest_driver['name'],
            "driver_id": nearest_driver['id'],
            "fair": round(distance_min*2, 0)
        }
        socket.emit('message', data, namespace='/confirmation')


@app.route('/rider', methods=['POST'])
def add_rider():
    data = request.json
    avail_riders.append(data)
    return flask.Response(status = 201)


@app.route('/driver', methods=['POST'])
def add_driver():
    data = request.json
    avail_drivers.append(data)
    return flask.Response(status=201)


@app.route('/rating', methods=['POST'])
def store_rating():
    connection = mysql.connector.connect(user='root', host='127.0.0.1', database='Rideshare')
    data = request.json
    cursor = connection.cursor()
    query = """INSERT INTO driver_rating (rider_id,rider_name,driver_id,driver_name,rating) VALUES (%s, %s, %s, %s, %s)"""
    qdata = (data['r_id'],data['rider_name'],data['d_id'],data['driver_name'],data['rating'])

    try:
        cursor.execute(query, qdata)
        connection.commit()
        print("success")

    except:
        print("lost")

    return flask.Response(status=201)