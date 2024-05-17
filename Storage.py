#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import uuid
import sqlite3

conn = sqlite3.connect("sms.db")
cur = conn.cursor()

class Storage:
    def AddNewMsg(sender,msg,recvtime):
        id=str(uuid.uuid4())
        data = [(id,sender,msg,recvtime,1)]
        cur.executemany(
            "insert into recvbox values(?,?,?,?,?)",data)
        conn.commit();
        print(recvtime+' > A new sms received! Check your inbox.')

    def InitDb():
        print(str(datetime.now())+' > Database Checking.')
        table_exist = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='recvbox'")#检查是否有recvbox这张表
        if table_exist.fetchone() is None:#没有则创建
            cur.execute(
                "create table if not exists recvbox (id varchar(50), sender nvarchar(50), msg TEXT, recvtime varchar(50), isunread integer)")
            conn.commit()    
            print(str(datetime.now())+' > Database initialized.')
        else:        #有则跳过
            print(str(datetime.now())+' > Database Checked over.')
