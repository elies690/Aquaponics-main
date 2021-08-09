from task_manager import TimeOrder, Task
import asyncio
import time
import task_manager
from pitcpserver import TcpServer
from MessageListener import MessageReceivedListener
from datetime import date,datetime

def task_1():
    print('task 1: '+ str(datetime.now()))

host = '192.168.1.65'
port = 8080

MsgListener = MessageReceivedListener()
tcpServer = TcpServer(host, port, MsgListener)

Task1 = Task('task1',task_1,5,TimeOrder.SECOND,'none')
task_manager.schedule_task(Task1)
   
async def main():                
        while True:
                manager = loop.create_task(task_manager.run())
                server = loop.create_task(tcpServer.start())
                await asyncio.wait([manager,server])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
