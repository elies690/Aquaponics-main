from time import sleep
import schedule
import task_manager
from task_manager import TimeOrder, Task
from datetime import date,datetime
import csv
import asyncio

class SystemController():

        def __init__(self,alarm,T_range,TDS_range,sendMessage=None):
                self.alarm = alarm
                self.T_range = T_range
                self.TDS_range = TDS_range
                self.t_high = None
                self.t_low = None
                self._timeBackUp = '/home/pi/Aquaponics/Data/Level/BackUp.csv'
                self._levelLogging = '/home/pi/Aquaponics/Data/Level/'
                self._pumpsLogging = '/home/pi/Aquaponics/Data/Pumps/'
                self.send_message = sendMessage
                self.nb_level = 2
                self._pumps_tag = 'pumps'

        def _get_time_backup(self,nb,state):
                file = open(self._timeBackUp,'r')
                reader = csv.reader(file)
                data = list(reader)
                file.close()
                return(data[nb][state])

        def _update_time(self,nb,ts,tag):
                file = open(self._timeBackUp,'r')
                reader = csv.reader(file)
                data = list(reader)
                file.close()
                data[nb][tag] = ts
                new = open(self._timeBackUp,'w')
                writer = csv.writer(new)
                writer.writerows(data)
                new.close()

        def _log_level(self,nb,dt,state):
                file = open(self._levelLogging + str(nb) + '.csv','a')
                tag_name = [1]
                time = [1]
                with file as csvfile:
                        tag_name[0] = state
                        time[0] = dt
                        csvwriter = csv.writer(csvfile, delimiter=',')
                        csvwriter.writerow(tag_name+time)

        def _log_pumps(self,nb,dt,state):
                file = open(self._pumpsLogging + str(nb) + '.csv','a')
                tag_name = [1]
                time = [1]
                with file as csvfile:
                        tag_name[0] = state
                        time[0] = dt
                        csvwriter = csv.writer(csvfile, delimiter=',')
                        csvwriter.writerow(tag_name+time)


        def level_manager(self,nb,state):

                if state == 0:
                        t_up = datetime.fromisoformat(self._get_time_backup(nb,1))
                        dt = (datetime.now()-t_up).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'high_up')
                        self._update_time(nb,str(datetime.now()),0)

                elif state == 1:
                        t_down = datetime.fromisoformat(self._get_time_backup(nb,0))
                        dt = (datetime.now()-t_down).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'high_down')
                        self._update_time(nb,str(datetime.now()),1)

                elif state == 2:
                        t_up = datetime.fromisoformat(self._get_time_backup(nb,3))
                        dt = (datetime.now()-t_up).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'low_up')
                        self._update_time(nb,str(datetime.now()),2)

                elif state == 3:
                        t_down = datetime.fromisoformat(self._get_time_backup(nb,2))
                        dt = (datetime.now()-t_down).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'low_down')
                        self._update_time(nb,str(datetime.now()),3)

        def switch_pumps(self):
                print('sw')
                asyncio.ensure_future(self.send_message('pump;sp;0'))

        async def pumps_manager(self,cmd):
                if cmd == 'Auto':
                        task_pumpsSwitch = Task("PumpsSwitch",self.switch_pumps,6,TimeOrder.SECOND,self._pumps_tag)
                        task_manager.schedule_task(task_pumpsSwitch)

                else:
                        task_manager.clear_tasks(self._pumps_tag)

        def manage_sensor_reading(self,temperature,tds):

                if temperature<self.T_range[1] and temperature>self.T_range[0]:
                        self.heater_on()
                        self.alarm.set_state(state=0)
                elif temperature<self.T_range[2] and temperature>self.T_range[1]:
                        self.heater_off()
                        self.alarm.set_state(state=0)
                elif temperature<self.T_range[0]:
                        self.alarm.set_state(state=2,msg="Water Temperature too low")
                elif temperature>self.T_range[2]:
                        self.alarm.set_state(state=2,msg="Water Temperature too high")

                if self.tds>self.TDS_range[1]:
                        self.alarm.set_state(state=2,msg="TDS level too high")

                elif self.tds<self.TDS_range[0]:
                        self.alarm.set_state(state=2,msg="TDS level too low")
