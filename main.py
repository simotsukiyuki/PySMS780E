#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
from time import sleep
import serial
import os
from serial.serialutil import EIGHTBITS, PARITY_NONE
from multiprocessing import Process
from SendMail import SendMail
from Storage import Storage
import Config

# 接收到短信时的处理程序
def SMSReceivedProcessing(smsrawdata):
    smsrawdata=smsrawdata.replace("@$","{\"")
    smsrawdata=smsrawdata.replace("$@","\"}")
    smsrawdata=smsrawdata.replace("$","\"")
    # 替换占位符为Json格式
    
    recvtime=str(datetime.now()) # 接收短信的时间=现在
    sender="";# 发件人
    smscontent="";# 短信内容
    
    try:        #解析json
        msg = json.loads(smsrawdata)
        sender=msg["from"]
        smscontent=msg["data"]
    except:# 解析json失败时，直接将JSON作为短信内容输出，避免丢短信
        sender="RAWDATA"
        smscontent="JSON PARSE FAILED. RAW DATA: "+smsrawdata
    finally:
        Storage.AddNewMsg(sender,smscontent,recvtime)# 存储短信到SQLITE3
        SendMail.SendNewMail(sender,smscontent,recvtime)# 发邮件的处理

# 主进程
def SMS780E():
    print(str(datetime.now())+' > Module name:', __name__)
    print(str(datetime.now())+' > Parent process:', os.getppid())
    print(str(datetime.now())+' > process id:', os.getpid())

    # 初始化Air780E用户串口
    ser = serial.Serial(Config.com_port,Config.com_baud,Config.com_bytesize,Config.com_parity)

    if ser.isOpen():#如果串口开启成功
        print(str(datetime.now())+" > UART communication success: "+ser.name)
        print(str(datetime.now())+" > To exit, press Ctrl+C")
    else:#串口开启失败，退出
        print(str(datetime.now())+" > UART communication Failed.")
        return

    while True:
        try:
            if ser.in_waiting:# 如果有数据传入（防止pyserial.read方法阻塞进程导致CPU占用过高）
                ser_in=ser.read(ser.in_waiting)# 读取指定长度的数据
                if ser_in:
                    SMSReceivedProcessing(ser_in.decode("utf-8"))# 数据传入以后将其转换为UTF-8格式，交给短信处理程序处理
            
            sleep(0.01)# 如果没有数据传入则等待0.01秒等待数据传入
            
        except KeyboardInterrupt:# Ctrl+C 退出
            ser.close()
            print(str(datetime.now())+" > Application Exit.")
            return

def main():
    Storage.InitDb() # 初始化数据库
    p_sms = Process(target=SMS780E) # 启动主进程
    p_sms.start()
    p_sms.join()
    
if __name__ == "__main__":
    main()