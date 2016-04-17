#!/usr/bin/env python
from flask import Flask, render_template, Response,redirect,request

# emulated camera
#from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

import serial
ser=serial.Serial('/dev/ttyACM0',9600)


app = Flask(__name__)



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/motion/')
def turn_right():
	#serial motion
    ser.write(request.query_string)
	return redirect('/')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
