from logging import warn, warning
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
                self._timeBackUp = 'C:/Users/User/Desktop/Files/Internship_YL/Aquaponics/Aquaponics-main/src/Aquaponics-pi/Data/Level/BackUp.csv'
                self._levelLogging = 'C:/Users/User/Desktop/Files/Internship_YL/Aquaponics/Aquaponics-main/src/Aquaponics-pi/Data/Level/Logging/'
                self._pumpsLogging = 'C:/Users/User/Desktop/Files/Internship_YL/Aquaponics/Aquaponics-main/src/Aquaponics-pi/Data/Pumps/Logging'
                self.sendMessage = sendMessage
                self.updateWebpage = updateWebpage
                self.nb_levels = 1
                self.levels = [self.nb_levels]

        def _get_time_backup(self,nb,state):
                file = open(self._timeBackUp,'r')
                reader = csv.reader(file)
                data = list(reader)
                print(data)
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

        def level_check(self):
                warning_msg = ''
                i=1
                for level in self.levels:
                        if level == 'low':
                                t_down = self._get_time_backup(nb,2)
                                dt = (datetime.now()-t_down).total_seconds()/60
                                if dt > self.time_interval_down:
                                        warning_msg+='level '+str(i)+ ' down too long'
                                

        def level_manager(self,nb,state):

                if state == 0:
                        t_up = datetime.fromisoformat(self._get_time_backup(nb,1))
                        dt = (datetime.now()-t_up).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'high_up')
                        self._update_time(nb,str(datetime.now()),0)
                        self.levels[nb-1]='mid'
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';0;'+str(dt)+';'+'mid'))

                elif state == 1:
                        t_down = datetime.fromisoformat(self._get_time_backup(nb,0))
                        dt = (datetime.now()-t_down).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'high_down')
                        self._update_time(nb,str(datetime.now()),1)
                        self.levels[nb-1]='up'
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';1;'+str(dt)+';'+'up'))

                elif state == 2:
                        t_up = datetime.fromisoformat(self._get_time_backup(nb,3))
                        dt = (datetime.now()-t_up).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'low_up')
                        self._update_time(nb,str(datetime.now()),2)
                        self.levels[nb-1]='low'
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';2;'+str(dt)+';'+'low'))

                elif state == 3:
                        t_down = datetime.fromisoformat(self._get_time_backup(nb,2))
                        dt = (datetime.now()-t_down).total_seconds()/60
                        print(dt)
                        self._log_level(nb,dt,'low_down')
                        self._update_time(nb,str(datetime.now()),3)
                        self.levels[nb-1]='mid'
                        asyncio.ensure_future(self.updateWebpage('level',str(nb)+';3;'+str(dt)+';'+'mid'))


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
                timestamp = str(datetime.now())
                asyncio.ensure_future(self.updateWebpage('pumps','1;'+str(pump)+';'+timestamp))
                self.active_pump = pump
                if mode:
                        task_pumpsSwitch = Task("PumpsSwitch",self.switch_pumps,6,TimeOrder.SECOND,'pumps')
                        task_manager.schedule_task(task_pumpsSwitch)
                        
                else:
                        task_manager.clear_tasks('pumps')

        def sensors_manager(self,temperature,tds):
                print('sensors manager')
                asyncio.ensure_future(self.updateWebpage('sensors',str(temperature) +';'+ str(tds)))
                warning_msg = ''
                if temperature<self.T_range[1] and temperature>self.T_range[0]:
                        warning_msg+='Water Temperature OK\n'
                elif temperature<self.T_range[2] and temperature>self.T_range[1]:
                        warning_msg+='Water Temperature OK\n'
                elif temperature<self.T_range[0]:
                        warning_msg+="Water Temperature too low\n"
                elif temperature>self.T_range[2]:
                        warning_msg+="Water Temperature too high\n"

                if tds>self.TDS_range[1]:
                        warning_msg+="TDS level too high\n"
                elif tds<self.TDS_range[0]:
                        warning_msg+="TDS level too low\n"
                else:
                        warning_msg+="TDS level OK\n"

                self.warnings_manager('sensors',warning_msg)

        def warnings_manager(self,tag,msg):
                if tag == 'pumps':
                        task_manager.clear_tasks('pumps')
                asyncio.ensure_future(self.updateWebpage('warnings',tag+';'+msg))