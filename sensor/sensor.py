# sensor.py
import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
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
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def main():
    try:
        while True:
            distance = measure_distance()
            print(f"Distance: {distance} cm")
            publish.single("parking/status", str(distance), hostname="localhost")
            time.sleep(2)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
