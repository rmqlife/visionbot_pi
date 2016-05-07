#!/usr/bin/env python
from flask import Flask, render_template, Response,redirect,request,send_file

# emulated camera
# from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)

import bluetooth
addr='30:14:11:17:21:57'
port=1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((addr,port))

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/motion/',methods=['POST','GET'])
def motion():
    cmd = request.args.get('cmd')
    sock.send(cmd+"\n")
    return render_template('index.html')

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

@app.route('/capture')
def capture():
    frame=Camera().get_frame()
    filename="test.jpg"
    file=open(filename,'w')
    file.write(frame)
    file.close()
    return send_file(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
