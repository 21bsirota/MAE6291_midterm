import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import json
import numpy as np
import plotly
import plotly.subplots
import plotly.express as px
from plotly.validator_cache import ValidatorCache
import time
import threading

import thing_file

SENSOR_1 = 16
SENSOR_2 = 18
NUM_HOLES = 32

app = Flask(__name__)

@app.route('/')
def run_flask():
    global data


    # ======================================================================    
    # ===== Create the graph with subplots with layout and margins =========
    # ======================================================================
    # fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)

    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    
    #last_time = time.time()
    
#     while True:
        
        #timeT = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        #data['Speed'].append(random.randint(0, 100))
        #data['timeT'].append(timeT)
        
#         if not GPIO.input(SENSOR):
#             print(1 / ((time.time() - last_time) * 60 / NUM_HOLES))
#             data['Speed'].append(1 / ((time.time() - last_time) * 60 / NUM_HOLES))
#             data['timeT'].append(time.time())
#             last_time = time.time()
#             while not GPIO.input(SENSOR):
#                 pass

        # ======================================================================    
        # ===== Create traces for plotly =======================================
        # ======================================================================
    fig.append_trace({
        'x': data['time1'],
        'y': data['Speed1'],
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    
    fig.append_trace({
        'x': data['time2'],
        'y': data['Speed2'],
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    # ======================================================================    
    # ===== Serializing fig json object ====================================
    # ===== Writing data into a json-file ==================================
    # ====================================================================== 

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # ======================================================================    
    # ===== Serializing raw data of Voltage and timeT into a json object ===
    # ===== Writing data into a json-file ==================================
    # ====================================================================== 
    json_object = json.dumps(data, sort_keys=True, default=str) 
#     print(json_object)
    with open("data.json", "a") as outfile:
        json.dump(json_object, outfile)
    
    # ======================================================================    
    # ===== Rendering data to the html frontend ============================
    # ====================================================================== 
    return render_template('template.html', graphJSON=graphJSON)

def get_data(data_id, sensor_pin):
    global data
    global init_time

    last_time = time.time()

    while True:
        if not GPIO.input(sensor_pin):
            #print('Sensor' + str(data_id) + ": " + str((1 / ((time.time() - last_time) * 60 / NUM_HOLES))) + "\n")
            speed = 1 / ((time.time() - last_time) * 60 / NUM_HOLES)
            current_time = time.time() - init_time
            if speed < 10000:
                data['Speed' + str(data_id)].append(speed)
                data['time' + str(data_id)].append(current_time)
                last_time = time.time()
            
            while not GPIO.input(sensor_pin):
                pass
    
    
def run_app():
    print()
    print('=======================================================')
    print('Welcome to My IoT device - %s' % thing_file.thing_name)
    print('http://localhost:5000')
    print('=======================================================')
    print()
    
    app.run(host="0.0.0.0", debug=True)

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SENSOR_1, GPIO.IN)
    GPIO.setup(SENSOR_2, GPIO.IN)
    

if __name__ == '__main__':
    global data
    global init_time
    data = {
        'time1': [],
        'Speed1': [],
        'time2': [],
        'Speed2': []
    }
    
    setup()
    
    init_time = time.time()
    
    t1 = threading.Thread(target=get_data, args=(1,SENSOR_1))
    t2 = threading.Thread(target=get_data, args=(2,SENSOR_2))
    
    t1.start()
    t2.start()
    
    run_app()