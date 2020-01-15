#!/bin/python3
from flask import *
import requests
import monitor
import _thread
import json
import timer
import time
import random
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("index.html")


monitor = monitor.Monitor()

@app.route('/device_data', methods=["GET", "POST"])
def device_data():
    if request.method == 'POST':
        dct = json.loads(request.get_data().decode())
        monitor.receive(dct)
        device = monitor.get_device_by_id(dct[0]['machine_id'])
        control = monitor.calc_control(device)
        return json.dumps(control.__dict__)

    else:  # GET
        return json.dumps(monitor.fetch_device_list())

@app.route('/run_motor')
def run_motor():
    machine_id = request.args.get('id')
    device = monitor.get_device_by_id(machine_id)
    if not device:
        return json.dumps({'error': 'Did not find a device with the id ' + str(machine_id)})
    device.motor = True
    return '{}'

@app.route('/problematic_devices')
def problematic_devices():
    return json.dumps(monitor.problematic_devices())


@app.route('/device_request', methods=['GET'])
def device_request():
    machine_id = request.args.get('id')
    device = monitor.get_device_by_id(machine_id)
    if not device:
        return json.dumps({'error': 'Did not find a device with the id ' + str(machine_id)})
    control = monitor.calc_control(device)
    return json.dumps(control.__dict__)

@app.route('/device_depr', methods=['GET'])
def device_depr():
    machine_id = request.args.get('id')
    device = monitor.get_device_by_id(machine_id)
    if not device:
        return json.dumps({'error': 'Did not find a device with the id ' + str(machine_id)})
    monitor.depr_device(device)
    return '{}'

@app.route('/device', methods=['GET'])
def device():
    return render_template("device.html")

@app.route('/device_history', methods=['GET'])
def device_history():
    machine_id = request.args.get('id')
    name = request.args.get('name')
    device = monitor.get_device_by_id(machine_id)
    tm = []
    val = []
    if device:
        for data in device.data[-20:]:
            try:
                val.append(data[name])
                tm.append(time.strftime("%H:%M:%S", time.gmtime(data['time'])))
            except _ as ignored:
                pass
    return json.dumps({'times':tm, 'values': val})
@app.route('/clock')
def clock():
    return str(time.time())
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
