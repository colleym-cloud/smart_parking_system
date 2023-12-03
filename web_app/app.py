 # app.py
from flask import Flask, render_template
import paho.mqtt.subscribe as subscribe

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', status=get_sensor_status())

def get_sensor_status():
    msg = subscribe.simple("parking/status", hostname="localhost")
    return msg.payload.decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
