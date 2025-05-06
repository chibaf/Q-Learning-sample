#!/usr/bin/python3
#
from datetime import date
import time
import matplotlib.pyplot as plt
import serial
import RPi.GPIO as GPIO
import os
import sys
import threading
import queue  # library for queu operation
from thread_one_class import thread_one  # import thread body
import random
#
it=1   # counter
thread1=thread_one(it) #provide a thread
q =queue.Queue()  # queue which stores a result of a thread
th = threading.Thread(target=thread1.thread, args=(it,q),daemon=True)
#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#
# Raspberry Pi pins vs SSR
# heater: 11(top),12(core),13(side upper),16(side lower),19(bottom)
# 5=pump, 18= freezer 
#
GPIO.setup(11, GPIO.OUT)  # side heater: : ssr11
GPIO.setup(12, GPIO.OUT)  # core heater: ssr12
GPIO.setup(13, GPIO.OUT)  # heater: ssr13
GPIO.setup(15, GPIO.OUT)  # pump: ssr15
GPIO.setup(16, GPIO.OUT)  # side heater: ssr16
GPIO.setup(18, GPIO.OUT)  # freezer: ssr18
GPIO.setup(19, GPIO.OUT)  # bottom heater: ssr19
#
from read_m5_class import m5logger
#
today = date.today()
t = time.localtime()
current_time = time.strftime("_H%H_M%M_S%S", t)
fn = "LOG-SSR_" + str(today) + current_time + ".csv"
f = open(fn, 'w', encoding="utf-8")
fq=open("QL-LOG.csv","w",encoding="utf-8")
start = time.time()
qlstart=start
#
ldata0 = [0] * 10
ldata = [ldata0] * 10
m5port = m5logger()
ser=serial.Serial("/dev/ttyUSB0",115200)
#
data03 = [0] * 10
data3 = [data03] * 10
ql=[0]*15
QL=[ql]*5
qlcnt=0
#
ssr11 = "0";ssr12 = "0";ssr13 = "0";ssr15 = "0";ssr16 = "0";ssr18 = "0";ssr19 = "0"; #switch flag
#
f18 = 0
fssr=0
flg = 0
t1 = 5
t2 = 5
iql=0
iq=0
th.start() # start thread
while True:
    try:
        ttime = time.time() - start
        if ttime < 0.001:
            ttime = 0.0
        if f18 == 0:
            ctime = ttime
            f18 = 1
        if fssr == 0:
            ftime = ttime
            fssr = 1
        if flg == 0:
            stime = ttime
            flg = 1
        st = time.strftime("%Y %b %d %H:%M:%S", time.localtime())
        ss = str(time.time() - int(time.time()))
        rttime = round(ttime, 2)
        array3 = m5port.read_logger(ser)
        sum3=0.0
        for i in range(0, 10):
           sum3 += abs(array3[i])
        if sum3 == 0.0:
            continue
        # heater on=2sec/off=8sec
        if stime + 10 < ttime:
            flg = 0
        if ftime+10<ttime:
            fssr=0
        if fssr==1:
          if ttime<ftime+2:
            ssr11="1";ssr12="1";ssr13="1";ssr16="1";ssr19="1";
            GPIO.output(11, 1) # 250331
            GPIO.output(12, 1)  # Turn on ssr12
            GPIO.output(13, 1) # 250331
            GPIO.output(16, 1) # 250331
            GPIO.output(19, 1) # 250331
          elif ftime+2<=ttime<=ftime+10:
            ssr11="0";ssr12="0";ssr13="0";ssr16="0";ssr19="0";
            GPIO.output(11, 0) # 250331
            GPIO.output(12, 0)  # Turn off ssr12
            GPIO.output(13, 0) # 250331
            GPIO.output(16, 0) # 250331
            GPIO.output(19, 0) # 250331
          else:
            fssr=0
# 
        if float(array3[0]) > -10.0:  # freezer on/off
            if ttime <= ctime + 1500.0:
                ssr18 = "1"
                GPIO.output(18, 1)
            if ctime + 1500 <= ttime <= ctime + 1800:
                ssr18 = "0"
                GPIO.output(18, 0)
            if ctime + 1800 < ttime:
                f18 = 0
        else:
            ssr18 = "0"
            GPIO.output(18, 0)
        GPIO.output(15, 1)  # pump on
        ssr15 = "1"       
#        
        ss = st + ss[1:5] + "," + str(rttime) + ","
#        
#        ar3=[array3[5],array3[6],array3[7],array3[8],array3[9],array3[15],array3[16],array3[17],array3[18],array3[19]]
        for i in range(0, len(array3) - 1):
            ss = ss + str(array3[i]) + ","
        ss = ss + str(array3[len(array3) - 1])+","
        ss=ss+ssr11+","+ssr12+","+ssr13+","+ssr15+","+ssr16+","+ssr18+","+ssr19+"\n"
        f.write(ss)
        if time.time()-qlstart>5.0:
          iql=iql+1
          sum1=0.0;sum2=0.0;
          for i in range(0,len(array3)):
            sum1=sum1+abs(array3[i])
          if sum1==0.0:
            continue
          elif iql>=5:
            QL1=array3+[int(ssr11),int(ssr12),int(ssr13),int(ssr16),int(ssr19)]
            QL.pop(-1)
            QL.insert(0,QL1)
            print(QL)
            iq=iq+1
            if iq>=5: 
              fq.write(str(QL)+"\n")
            qlstart=time.time()
          if iql>=5:
            print(iql)
            if th.is_alive()==False:  #when thread ends
              result = q.get()  # take queu values
              print("thread: "+str(it)+" "+str(result))
              it=it+1
              if it<6:
                thread1=thread_one(it) #proivide the next thread
                th = threading.Thread(target=thread1.thread, args=(it,q),daemon=True)
              # setting the next thread
                th.start() # start thread
#            if it>5:  # execute total five thread 
#              break;  # exit loop
        sumar3=0
        for i in range(0,10):
          sumar3=sumar3+array3[i]
        if sumar3==0:
          continue
        data3.pop(-1)
        data3.insert(0, array3)
        rez3 = [[data3[j][i] for j in range(len(data3))] for i in range(len(data3[0]))]  # transposing a matrix
#          plotting
        x = range(0, 10, 1)
#       
        plt.figure(100)
        plt.clf()
        plt.ylim(-40, 40)
        tl3 = [0] * 10
        h3 = []
        for i in range(0, 10):
           tl3[i], = plt.plot(x, rez3[i], label="T" + str(i))
        for i in range(0, 10):
          h3.append(tl3[i])
        plt.legend(handles=h3)
        plt.pause(0.1)
#        
#          x = range(0, 10, 1)
#        plt.figure(110)
#        plt.clf()
#        plt.ylim(-40, 40)
#        tl4 = [0] * 5
#        h4 = []
#        for i in range(0,5):
#          y=rez3[i+5]
#          y2=y[0:10]
#          tl4[i], = plt.plot(x, y2, label="T" + str(i))
#        for i in range(0, 5):
#          h4.append(tl4[i])
#        plt.legend(handles=h4)
#        plt.pause(0.1)
#        
    except KeyboardInterrupt:
        GPIO.output(11, False)
        GPIO.output(12, False)
        GPIO.output(13, False)
        GPIO.output(15, False)
        GPIO.output(16, False)  #0321
        GPIO.output(18, False)
        GPIO.output(19, False)
        f.close()
        fq.close()
        ser3.close()
#        ser4.close()
        exit()
