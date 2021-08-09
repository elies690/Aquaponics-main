from Alarm import Alarm
from SystemController import SystemController
import task_manager
from task_manager import TimeOrder, Task
from pitcpserver import TcpServer
import asyncio
from MessageListener import MessageReceivedListener

host = '192.168.1.67'
port = 8080

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

##def control_loop(system_controller,data_acquisition):
##	[temperature,tds] = data_acquisition.get_sensor_data()
##	system_controller.manage_sensor_data(temperature,tds)

def demo():
        print("read sensors...")
        

#Create the controllers and managers needed
alarm = Alarm(alarmLed,alarmBuzzer,alarmBtn)	
system_controller = SystemController(alarm,T_range,TDS_range)

#Create the tasks
task_sensorsControl = Task('SensorsControl',demo,10,TimeOrder.SECOND,'sensors')

#Schedule tasks
task_manager.schedule_task(task_sensorsControl)

#Create tcpServer and messageListener
MsgListener = MessageReceivedListener(system_controller)
tcpServer = TcpServer(host, port, MsgListener)
system_controller.send_message = tcpServer.send_message

async def main():                
        while True:
                manager = loop.create_task(task_manager.run())
                server = loop.create_task(tcpServer.start())
                await asyncio.wait([manager,server])

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
