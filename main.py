#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
from time import sleep
import serial
import os
from serial.serialutil import EIGHTBITS, PARITY_NONE
from multiprocessing import Process
from SendMail import SendMail
from Storage import Storage
import Config, GlobalData

# 将SMS780E的伪JSON转换为真JSON
# 参考资料：https://github.com/simotsukiyuki/sms_forwarding_uart
# 输入：smsrawdata: SMS780E的伪JSON, string
# 输出：真正的短信JSON
def SMSRawDataToRealJson(smsrawdata):
    smsrawdata=smsrawdata.replace("@$","{\"")
    smsrawdata=smsrawdata.replace("$@","\"}")
    smsrawdata=smsrawdata.replace("$","\"")
    # 替换占位符为Json格式    
    return smsrawdata

# 发送短信
# 输入：sendto：信息收件人号码 smscontent：信息内容 serialObject：pySerial的用户串口对象（必须！）
def SendSms(sendto,smscontent,serialObject):
    if datetime.now()>=GlobalData.nextSmsSendAccept:# 如果已经过了冷却时间
        print(str(datetime.now())+' > SMS is sending...')
        jsonData=str('{"type":"sms","to":"'+ sendto +'","content":"'+ smscontent +'"}')# 拼接json，具体参考https://github.com/simotsukiyuki/sms_forwarding_uart
        serialObject.write(jsonData.encode())# 将json字符串转换为pySerial能接收的bytes并且发送到用户串口
        GlobalData.nextSmsSendAccept=datetime.now()+timedelta(seconds=Config.smscmd_cmd_nextsms_countdown)# 刷新冷却时间
        print(str(datetime.now())+' > SMS send completed. Next SMS could be send at: ', GlobalData.nextSmsSendAccept)
    else:# 如果还在冷却时间则跳过
        print(str(datetime.now())+' > SMS not send dual cold-down, until time: ', GlobalData.nextSmsSendAccept)
    return

# 接收到短信时的处理程序
# 只能接受正确格式的JSON，不支持SMS780E直接输出的伪JSON
# 输入：smsrawdata: 处理后的JSON, string
def SMSReceivedProcessing(smsrawdata):
    recvtime=str(datetime.now()) # 接收短信的时间=现在
    sender="";# 发件人
    smscontent="";# 短信内容
    
    try:        #解析json
        msg = json.loads(smsrawdata) # JSON->msg对象
        sender=msg["from"]
        smscontent=msg["data"]
    except:# 解析json失败时，直接将JSON作为短信内容输出，避免丢短信
        sender="RAWDATA"
        smscontent="JSON PARSE FAILED. RAW DATA: "+smsrawdata
    finally:
        Storage.AddNewMsg(sender,smscontent,recvtime)# 存储短信到SQLITE3
        SendMail.SendNewMail(sender,smscontent,recvtime)# 发邮件的处理

# 短信指令处理程序
def SMSCmdProcessing(smsrawdata,serialObject):
    if Config.smscmd_enable == False:# 如果短信指令功能未开启则跳过
        return False
    else:
        try:
            msg = json.loads(smsrawdata) # JSON->msg对象
            if msg["from"] in Config.smscmd_admin_phone : # 如果短信的发件人是管理员
                cmds=str(msg["data"]).split(Config.smscmd_cmd_split_flag,2)# 按格式将短信指令进行分割
                cmd=cmds[0]# 短信指令
                print(str(datetime.now())+' > Received Administrator SMS: ', cmds)

                if cmd in Config.smscmd_command_sendsms:#发短信
                    sendto=str(cmds[1])# 收件人
                    content=str(cmds[2])# 短信内容
                    SendSms(sendto,content,serialObject)

                    return True
                elif cmd in Config.smscmd_command_exit:#退出
                    print(str(datetime.now())+' > Executing: ', cmd)
                    serialObject.close()

                    return True
                else:
                    print(str(datetime.now())+' > Unknown Command: ', cmd)
                    
                    return False;
            else:# 不是管理员则忽略此短信
                print(str(datetime.now())+' > NOT SMS Command or Not Administrator. Skip.')
                return False
        except Exception as e:
            print(str(datetime.now())+" > SMS Command Exec Failed! ",e)
            return False

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
                    ser_in_utf8=SMSRawDataToRealJson(ser_in.decode("utf-8"))# 数据传入以后将其转换为UTF-8格式
                    cmd_process=SMSCmdProcessing(ser_in_utf8,ser)
                    if cmd_process==False or Config.smscmd_save_cmdsms:
                        SMSReceivedProcessing(ser_in_utf8)# 交给短信转发处理程序处理
            
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
    GlobalData.nextSmsSendAccept = datetime.now()# 刷新CD
    main()