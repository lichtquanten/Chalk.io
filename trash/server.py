from simple import SampleListener
import Leap, sys, gevent
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,async_mode='gevent', ping_timeout=30, logger=False, engineio_logger=False)
controller = None
listener = None
listener_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.before_first_request
def start_listener():
    global controller, listener, listener_thread

    def new_frame(counter):
        pass

    def new_point(point):
        print "New point"
        print point
        emit('new_point', point, namespace='/test')

    def send_message(message):
        print "sending"
        emit('message', message)
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
    listener = SampleListener(new_frame_cb = new_frame, new_point_cb = new_point, send_message = send_message)
    listener_thread = Thread(target = controller.add_listener, args = (listener, ))
    print "start"
    listener_thread.daemon = True
    listener_thread.start()
    print "ayo started"

@socketio.on('connect', namespace='/test')
def connect():
    print "New connection"
    emit('message', "yo")


if __name__ == '__main__':
    server_thread = Thread(target = socketio.run, args = (app,), kwargs = {'host': '127.0.0.1', 'port': 5000})
    server_thread.daemon = True
    server_thread.start()

    # Keep this process running until Enter is pressed
    print "Press Enter to quit...BOIIII"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        #controller.remove_listener(listener)
        pass
