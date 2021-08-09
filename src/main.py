from Alarm import Alarm
from SystemController import SystemController
import task_manager
from task_manager import TimeOrder, Task
from pitcpserver import TcpServer
from socketIO_client import sio_AsyncClient
import asyncio
from MessageListener import MessageReceivedListener

tcp_host = '192.168.0.120'
tcp_port = 8080

sio_host = '192.168.0.120'
sio_port = 9999

# Initializing parameters
##################################
alarmLed = 11
alarmBuzzer =10
alarmBtn = 12
heater_pin = 15
T_range = (30,40,50)
TDS_range = (1000,1400,2000)
tempPin = 20
tdsPin = 24
##################################

#Create the controllers and managers needed
alarm = Alarm(alarmLed,alarmBuzzer,alarmBtn)	
system_controller = SystemController(alarm,T_range,TDS_range)

#Create tasks
task_getSensors = Task('GetSensors',system_controller.get_sensors_readings,10,TimeOrder.SECOND,'sensors')
task_feederRun = Task('FeederRun',system_controller.run_feeder,15,TimeOrder.SECOND,'feeder')
task_levelCheck = Task('LevelCheck',system_controller.level_check,5,TimeOrder.SECOND,'level')

#Schedule tasks
task_manager.schedule_task(task_getSensors)
task_manager.schedule_task(task_feederRun)
task_manager.schedule_task(task_levelCheck)

#Create tcpServer and messageListener
MsgListener = MessageReceivedListener(system_controller)
tcpServer = TcpServer(tcp_host, tcp_port, MsgListener)
sio_client = sio_AsyncClient(sio_host,sio_port)

system_controller.sendMessage = tcpServer.send_message
system_controller.updateWebpage = sio_client.update_webpage
sio_client.controller = system_controller

async def main():
        while True:
                manager = loop.create_task(task_manager.run())
                server = loop.create_task(tcpServer.start())
                web = loop.create_task(sio_client.connect())
                await asyncio.wait([manager,server,web])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
