#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmail
import Config


if __name__ == "__main__":
    server = zmail.server(username=Config.smtp_login_account,
                          password=Config.smtp_login_password,
                          smtp_host=Config.smtp_server,
                          smtp_port=Config.smtp_port,
                          smtp_ssl=Config.smtp_ssl,
                          smtp_tls=Config.smtp_tls)

    mail = {
        'from': Config.smtp_mail_sender_name+' <'+Config.smtp_mail_sender_address+'>',
        'to': Config.smtp_mail_receiver_name+' <'+Config.smtp_mail_receiver_address+'>',
        'subject': 'Welcome to PySMS780E!',
        'content_text': 'Congratulations! The email configuration is finished and you can receive your sms with email now.',
    }
    if server.smtp_able():
        pass
    
    server.send_mail(Config.smtp_mail_receiver_address,mail)
    
    print("E-Mail Send Complete. Check your inbox.")