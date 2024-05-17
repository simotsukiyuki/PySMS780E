#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from serial.serialutil import EIGHTBITS, PARITY_NONE

com_port = "COM3" # User UART port of780E
com_baud = 115200 # baud rate
com_bytesize = EIGHTBITS # byte size
com_parity = PARITY_NONE # parity

smtp_enable=False # Enable/Disable email function
smtp_server="mail.example.com" # Email server
smtp_ssl=True # Use SSL or not (DO NOT ENABLE WITH TLS AT SAME TIME)
smtp_tls=False # use tls or not (DO NOT ENABLE WITH SSL AT SAME TIME)
smtp_port=465 # email service network port
smtp_login_account="somebody@example.com" # Login account
smtp_login_password="ABCD1234" # password
smtp_mail_sender_address="somebody@example.com" # email address which will shown in the sender
smtp_mail_sender_name="SENDER Name" # name which will shown in the sender
smtp_mail_receiver_address="somebody@example.com" # email address which will shown in the receiver
smtp_mail_receiver_name="RECEIVER Name" # name address which will shown in the receiver

mail_title_content="新消息来自" # New SMS From
mail_body_content=""
mail_end_content="消息接收时间：" # SMS was received at: