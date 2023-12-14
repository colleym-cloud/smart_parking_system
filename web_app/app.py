 # app.py
from flask import Flask, render_template
import RPi.GPIO as GPIO
import time
from gunicorn_config import bind, workers



app = Flask(__name__)

TRIG = 17  # GPIO17
ECHO = 18  # GPIO18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 343m/s, and there and back.
    distance = round(distance, 2)

    return distance

@app.route('/')
def index():
    distance = get_distance()
    status = "Occupied" if distance < 10 else "Free"
    return render_template('index.html', distance=distance, status=status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)