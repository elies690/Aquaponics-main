import socketio

class sio_AsyncClient():

    def __init__(self,host,port):
        self._port = port
        self._host = host
        self.CONNECTED = False
        self.sio_client = socketio.AsyncClient()

    async def connect(self):
        if not self.CONNECTED:
            url = 'http://' + self._host +':'+ str(self._port)
            await self.sio_client.connect(url)
            self.CONNECTED = True

    async def emit_event(self,event,message):
        await self.sio_client.emit(event,message)