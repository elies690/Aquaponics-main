import socketio

class socketIO_client():
    def __init__(self,host,port):
        self._host = host
        self._port = port
        self.socket = socketio.Client()

    def connect(self):
        url = self._host + ':' + str(self._port)
        self.socket.connect(url)

    def update_webpage(self,event,message):
        self.socket.emit(event,message)

socket = socketio.Client()
socket.connect('192.168.1.65:9999')
socket.wait()
