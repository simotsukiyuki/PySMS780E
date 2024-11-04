#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import zmail
import Config

class SendMail:
    def SendNewMail(sms_sender,sms_content,sms_recvtime):
        if(Config.smtp_enable == False):
            return
        else:
            print(str(datetime.now())+" > Sending E-Mail.")
            
        try:            
            title = Config.mail_title_content+" ["+sms_sender+"]"
            content = Config.mail_body_content + sms_content + "\n" + Config.mail_end_content + sms_recvtime
            server = zmail.server(username=Config.smtp_login_account,
                                  password=Config.smtp_login_password,
                                  smtp_host=Config.smtp_server,
                                  smtp_port=Config.smtp_port,
                                  smtp_ssl=Config.smtp_ssl,
                                  smtp_tls=Config.smtp_tls)

            mail = {
                'from': Config.smtp_mail_sender_name+' <'+Config.smtp_mail_sender_address+'>',
                'to': Config.smtp_mail_receiver_name+' <'+Config.smtp_mail_receiver_address+'>',
                'subject': title,
                'content_text': content,
            }
            if server.smtp_able():
                pass
    
            server.send_mail(Config.smtp_mail_receiver_address,mail)
    
            print(str(datetime.now())+' > E-Mail Send Complete.')
        except Exception:
            print(str(datetime.now())+" > E-Mail Send Failed.")
        