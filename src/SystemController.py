from os import times
from time import sleep, time
import schedule
import task_manager
from task_manager import TimeOrder, Task
from datetime import date,datetime
import csv
import asyncio

class SystemController():

        def __init__(self,alarm,T_range,TDS_range,sendMessage=None,updateWebpage=None):
                self.alarm = alarm
                self.T_range = T_range
                self.TDS_range = TDS_range
                self.t_high = None
                self.t_low = None
                self._timeBackUp = '/home/pi/Aquaponics_pi/Data/Level/BackUp.csv'
                self._levelLogging = '/home/pi/Aquaponics_pi/Data/Level/'
                self._pumpsLogging = '/home/pi/Aquaponics_pi/Data/Pumps/'
                self.sendMessage = sendMessage
                self.updateWebpage = updateWebpage
                self.nb_level = 2
                self.active_pump = ''

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
                        
                        t_2 = datetime.fromisoformat(self._get_time_backup(nb,1))
                        dt = (datetime.now()-t_2).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'mid')
                        self._update_time(nb,str(datetime.now()),1)
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';1;'+str(dt)+';low'))

                elif state == 1:
                        t_1 = datetime.fromisoformat(self._get_time_backup(nb,0))
                        dt = (datetime.now()-t_1).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'down')
                        self._update_time(nb,str(datetime.now()),0)
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';0;'+str(dt)+';mid'))

                elif state == 2:
                        t_2 = datetime.fromisoformat(self._get_time_backup(nb,1))
                        dt = (datetime.now()-t_2).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'up')
                        self._update_time(nb,str(datetime.now()),1)
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';2;'+str(dt)+';up'))

                elif state == 3:
                        t_1 = datetime.fromisoformat(self._get_time_backup(nb,0))
                        dt = (datetime.now()-t_1).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'mid')
                        self._update_time(nb,str(datetime.now()),0)
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';1;'+str(dt)+';mid'))


        def switch_pumps(self):
                print('pumps;switch')
                asyncio.ensure_future(self.sendMessage('pumps;sp;0'))

        def get_sensors_readings(self):
                print('sensors;get')
                asyncio.ensure_future(self.sendMessage('sensors;get;0'))

        def run_feeder(self):
                print('feeder;run')
                asyncio.ensure_future(self.sendMessage('feeder;run;0'))
                
        def pumps_manager(self,mode,pump):
                if mode:
                        task_pumpsSwitch = Task("PumpsSwitch",self.switch_pumps,6,TimeOrder.SECOND,'pumps')
                        task_manager.schedule_task(task_pumpsSwitch)
                        timestamp = str(datetime.now().time())
                        asyncio.ensure_future(self.updateWebpage('pumps','1;'+pump+';'+timestamp))

                else:
                        task_manager.clear_tasks('pumps')
                        timestamp = str(datetime.now().time())
                        asyncio.ensure_future(self.updateWebpage('pumps','0;'+pump+';'+timestamp))

        def sensors_manager(self,temperature,tds):
                print('sensors manager')
                asyncio.ensure_future(self.updateWebpage('sensors',str(temperature) +';'+ str(tds)))

                if temperature<self.T_range[1] and temperature>self.T_range[0]:
                        self.alarm.set_state(state=0)
                elif temperature<self.T_range[2] and temperature>self.T_range[1]:
                        self.alarm.set_state(state=0)
                elif temperature<self.T_range[0]:
                        self.alarm.set_state(state=2,msg="Water Temperature too low")
                elif temperature>self.T_range[2]:
                        self.alarm.set_state(state=2,msg="Water Temperature too high")

                if tds>self.TDS_range[1]:
                        self.alarm.set_state(state=2,msg="TDS level too high")

                elif tds<self.TDS_range[0]:
                        self.alarm.set_state(state=2,msg="TDS level too low")

        def warnings_manager(self,tag,msg):
                asyncio.ensure_future(self.updateWebpage('warnings',tag+';'+msg))