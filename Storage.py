#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import uuid
import sqlite3

conn = sqlite3.connect("sms.db")
cur = conn.cursor()

def AddNewMsg(sender,msg):
    id=str(uuid.uuid4())
    recvtime=str(datetime.now())
    data = [(id,sender,msg,recvtime,1)]
    cur.executemany(
        "insert into recvbox values(?,?,?,?,?)",data)
    conn.commit();

table_exist = cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='recvbox'")
if table_exist.fetchone() is None:
    cur.execute(
        "create table if not exists recvbox (id varchar(50), sender nvarchar(50), msg TEXT, recvtime varchar(50), isunread integer)")
    conn.commit()

AddNewMsg("666","999")

