from task_manager import TimeOrder, Task
import csv
from datetime import date,datetime
import csv
import task_manager

class MessageReceivedListener():

    def __init__(self):
        pass
        
    def OnMessageReceived(self, message):
        if message == '':
            pass
        else:
            self._handleMessage(message)

    def task_2(self):
        print('task 2: '+ str(datetime.now()))
        
    def _handleMessage(self,message):
        msg = message.split(";")
        tag = msg[0]
        data = msg[1:-1]
        print(message)

        if tag == "add":
            Task2 = Task('task2',self.task_2,3,TimeOrder.SECOND,'pumps')
            task_manager.schedule_task(Task2)
            
        elif tag == "remove":
            task_manager.clear_tasks('pumps')
