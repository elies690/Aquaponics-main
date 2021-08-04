from socket_client import socketIO_client
import asyncio
web_host = '192.168.1.65'
web_port = 9999

sio_client = socketIO_client(web_host,web_port)
sio_client.connect()

##async def main():
##        while True:
##                web = loop.create_task(sio_client.connect())
##                await asyncio.wait([web])
##
##loop = asyncio.get_event_loop()
##loop.run_until_complete(main())
##loop.close()
