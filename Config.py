#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from serial.serialutil import EIGHTBITS, PARITY_NONE

com_port = "COM3" # User UART port of 780E / 780E的用户串口
com_baud = 115200 # baud rate / 串口波特率
com_bytesize = EIGHTBITS # byte size / 串口数据位
com_parity = PARITY_NONE # parity / 串口校验位

smtp_enable=False # Enable/Disable email function / 是否启用邮箱转发
smtp_server="mail.example.com" # Email server / 邮箱服务器地址
smtp_ssl=True # Use SSL or not (DO NOT ENABLE WITH TLS AT SAME TIME) / 是否启用SSL，不要和TLS同时开启
smtp_tls=False # use tls or not (DO NOT ENABLE WITH SSL AT SAME TIME) / 是否启用TLS，不要和SSL同时开启
smtp_port=465 # email service network port / 邮件端口，开启SSL基本都是465
smtp_login_account="somebody@example.com" # Login account / 登录邮箱地址
smtp_login_password="ABCD1234" # password / 授权码
smtp_mail_sender_address="somebody@example.com" # email address which will shown in the sender / 发件人地址
smtp_mail_sender_name="SENDER Name" # name which will shown in the sender / 发件人
smtp_mail_receiver_address="somebody@example.com" # email address which will shown in the receiver / 收件人地址
smtp_mail_receiver_name="RECEIVER Name" # name address which will shown in the receiver / 收件人

mail_title_content="新消息来自" # New SMS From / （用于多语言翻译）邮件抬头
mail_body_content=""
mail_end_content="消息接收时间：" # SMS was received at: / （用于多语言翻译）邮件结尾

smscmd_enable=False # SMS Command Enable / 是否激活短信指令功能
smscmd_save_cmdsms=False # Save and forward Command SMS Enable / 是否保存并转发指令短信
smscmd_admin_phone="12345678901" # Administrator's Phone Number / 允许接受短信指令的管理号码
smscmd_cmd_split_flag="#" # Split Flag of SMS Command / 指令的分隔符
smscmd_cmd_nextsms_countdown=30 # Cold-Down time(seconds) of sending Next SMS / 连续发送短信指令的间隔时间，单位为秒
smscmd_command_sendsms="sms780e_sendto" # Command title of sending sms / 发送短信的指令
smscmd_command_exit="sms780e_exit" # Command title of stop server / 退出的指令
'''
Hint: The default COM_PORT of Air780E couldn't view in Windows, but you can check it with Luatools.
The default COM_PORT of Air780E in Linux is usually /dev/ttyACM3
提示：Air780E的默认COM口无法在Windows系统内确定，但你可以通过Luatools查看到。
Air780E的默认COM口在Linux操作系统下一般是/dev/ttyACM3
'''