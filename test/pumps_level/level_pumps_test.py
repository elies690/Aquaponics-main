from pitcpserver import TcpServer
import asyncio
from MessageListener import MessageReceivedListener
from datetime import date,datetime
import csv
import time

host = '192.168.1.65'
port = 8080

def _get_time_backup(nb,state):
    file = open('/home/pi/Aquaponics/Data/BackUp.csv','r')
    reader = csv.reader(file)
    data = list(reader)
    file.close()
    return(data[nb][state])

def _update_time(nb,ts,tag):
    file = open('/home/pi/Aquaponics/Data/BackUp.csv','r')
    reader = csv.reader(file)
    data = list(reader)
    file.close()
    data[nb][tag] = ts
    new = open('/home/pi/Aquaponics/Data/BackUp.csv','w')
    writer = csv.writer(new)
    writer.writerows(data)
    new.close()

def _log_level(nb,dt,state):
    file = open('/home/pi/Aquaponics/Data/Logging/'+str(nb)+'.csv','a')
    tag_name = [1]
    time = [1]
    with file as csvfile:
        tag_name[0] = state
        time[0] = dt
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(tag_name+time)

def level_manager(nb,state):
    if state == 1:
        t_down = datetime.fromisoformat(_get_time_backup(nb,0))
        print(t_down)
        dt = (datetime.now()-t_down).total_seconds()/60
        print(dt)
        _log_level(nb,dt,'down')
        _update_time(nb,str(datetime.now()),1)

    elif state == 0:
        t_up = datetime.fromisoformat(_get_time_backup(nb,1))
        dt = (datetime.now()-t_up).total_seconds()/60
        print(dt)
        _log_level(nb,dt,'up')
        _update_time(nb,str(datetime.now()),0)

    

def pumps_manager(msg):
    print(msg)

message_listener = MessageReceivedListener(level_manager,pumps_manager)
tcpServer = TcpServer(host, port, message_listener)

while 1:
        asyncio.run(tcpServer.start())

