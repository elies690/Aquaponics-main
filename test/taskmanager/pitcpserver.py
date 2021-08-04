import asyncio
from MessageListener import MessageReceivedListener
import time

class TcpServer():

    def __init__(self, host, port, messageReceivedHandler):
        ## add null checks and type checks here
        self._host = host
        self._port = port
        if not isinstance(messageReceivedHandler, MessageReceivedListener):
            raise Exception("Handler should be of type MessageReceviedListener") 
        self._handler = messageReceivedHandler
        self.serve = True
        
    async def _handleMessage(self, reader, writer):
        request = None
        cancel = False
        
        while self.serve:
            message = (await reader.read(255)).decode()
            if message == "quit":
                self.serve = False
            elif message != '':
                self._handler.OnMessageReceived(message)

        print("writerclosed")
        writer.close()

    async def send_message(self,msg):
        reader, writer = await asyncio.open_connection(self.host,self.port)
        writer.write(msg.encode())
        writer.close()

    async def start(self):
        try:
            server = await asyncio.start_server(self._handleMessage, self._host, self._port)
            self.serve = True
            addr = server.sockets[0].getsockname()
            print(f'Serving on {addr}')
            await server.start_serving()

        except OSError:
            pass
                
