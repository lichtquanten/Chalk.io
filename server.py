from listener import Listener
from flask import Flask, render_template
from flask_sockets import Sockets
from threading import Thread
import Leap


app = Flask(__name__, static_url_path='/static')
sockets = Sockets(app)

ws_send_lst = []

def send(message):
    for ws_send in ws_send_lst:
        ws_send(message)

@sockets.route('/echo')
def echo_socket(ws):
    index = len(ws_send_lst)
    ws_send_lst.append(ws.send)
    while not ws.closed:
        pass
    print "deleting!"
    del ws_send_lst[index]

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)
listener = Listener(send=send)
listener_thread = Thread(target = controller.add_listener, args = (listener, ))
listener_thread.start()




@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
