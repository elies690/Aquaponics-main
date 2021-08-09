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
            @self.sio_client.on('web')
            def print(message):
                print(message)
            self.CONNECTED = True

    async def update_webpage(self,event,message):
        await self.sio_client.emit(event,message)