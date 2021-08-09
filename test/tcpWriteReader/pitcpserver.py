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
                msg = message.split(";")
                tag = msg[0]
                if tag == 'pump':
                    self.pump_writer = writer
                elif tag == 'level':
                    self.level_write = writer
                
                self._handler.OnMessageReceived(message)

        print("writer closed")
        writer.close()

    async def send_message(self,message):
        msg = message.split(";")
        tag = msg[0]
        if tag == 'pump':   
            self.pump_writer.write(message.encode())
            await self.pump_writer.drain()

        elif tag == 'level':   
            self.level_writer.write(message.encode())
            await self.level_writer.drain()
            
        
    async def start(self):
        try:
            server = await asyncio.start_server(self._handleMessage, self._host, self._port)
            self.serve = True
            addr = server.sockets[0].getsockname()
            print(f'Serving on {addr}')
            await server.start_serving()

        except OSError:
            pass
                
