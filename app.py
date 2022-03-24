import os
import os.path
from datetime import datetime
from wsgiref.util import request_uri
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from dronekit import connect
import json

UPLOAD_FOLDER = 'file/'
# ALLOWED_EXTENSIONS = {'txt', 'waypoints', 'plan', 'mission'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_():
    return render_template("upload.html")

@app.route('/success', methods=['GET', 'POST']) 
def success(): 
    if request.method=='POST':
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        upload_file.save(app.config['UPLOAD_FOLDER'] + filename)
        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
    return render_template("success.html", name=upload_file.filename)

@app.route('/upload', methods=['GET'])
def upload():
    data = request.json
    print(data)
    current_time = datetime.now()
    microsecond = current_time.microsecond
    filename = 'datafile'+str(microsecond)+'.json'
    file_exists = os.path.exists(filename)
    if not file_exists:
        file = open(filename, 'w')
        file.write(json.dumps(data))
        file.close()
    return jsonify(data)


@app.route('/upload/mission', methods=['POST'])
def uploadmk():
    data = request.json
    #print(data)
    print(str(data['data']))
    current_time = datetime.now()
    microsecond = current_time.microsecond
    filename = 'datafile'+str(microsecond)+'.csv'
    file_exists = os.path.exists(filename)
    if not file_exists:
        file = open(filename, 'w')
        file.write(str(data['data']))
        file.close()
    return jsonify(data)

@app.route("/data", methods=['GET', 'POST'])
def index_data():
    # vehicle = connect('127.0.0.1:14550', wait_ready=True)
    vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=57600)

    mode = vehicle.mode.name
    global_location = vehicle.location.global_frame
    global_location_relative_altitude = vehicle.location.global_relative_frame
    local_location = vehicle.location.local_frame
    vehicle_altitude = vehicle.attitude
    vehicle_velocity = vehicle.velocity
    vehicle_gps_0 = vehicle.gps_0
    ground_speed = vehicle.groundspeed
    air_speed = vehicle.airspeed
    battery = vehicle.battery
    heart_beat = vehicle.last_heartbeat
    range_finder = vehicle.rangefinder
    range_finder_distance = vehicle.rangefinder.distance
    range_finder_voltage = vehicle.rangefinder.voltage
    heading = vehicle.heading
    arm_status = vehicle.is_armable
    system_status = vehicle.system_status.state
    print(mode)

    
    return jsonify({'mode':mode,
                    'globalLocation':{'latitude':global_location.lat ,'longitude':global_location.lon ,'altitude':global_location.alt},
                    'globalLocationRelativeAltitude':{'relativeLatitude':global_location_relative_altitude.lat, 'relativeLongitude': global_location_relative_altitude.lon, 'relativeAltitude':global_location_relative_altitude.alt},
                    'localLocation': {'north':local_location.north, 'east':local_location.east, 'down':local_location.down},
                    'vehicleAltitude': {'pitch':vehicle_altitude.pitch, 'yaw':vehicle_altitude.yaw, 'roll':vehicle_altitude.roll},
                    'vehicleVelocity': vehicle_velocity,
                    'GPS':{'fix':vehicle_gps_0.fix_type, 'satellites': vehicle_gps_0.satellites_visible},
                    'groundSpeed':ground_speed,
                    'airSpeed':air_speed,
                    'battery':{'voltage':battery.voltage, 'current':battery.current, 'percentage':battery.level},
                    'heartBeat':heart_beat,
                    'rangeFinder':{'distance':range_finder.distance, 'voltage':range_finder.voltage},
                    'heading':heading,
                    'armStatus':arm_status,
                    'systemStatus': system_status})


if __name__ == "__main__":
    app.run(port=2727, debug=True)