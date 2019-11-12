# -*- coding: utf-8 -*-
# __author__ = 'yafengstark'

# 这是中文注释
import sqlite3
import matplotlib.pyplot as plt
import shutil


def is_exists(dbPath, qk):
    """
    qk是否存在于db中
    :param dbPath:
    :param qk:
    :return:
    """
    b = False

    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("SELECT count(*) from tiles where qk = "+ qk)

    for row in cursor:
        count = row[0]
        if count>0:
            b = True

    conn.close()
    return b

# sql = ("INSERT INTO tiles(qk, data) VALUES (%s,%r)" %(A,B,A,B,B,A,A,B,C))
def insert(dbPath, qk, buffer):
    """

    :param dbPath:
    :param rar:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    print("Opened database successfully")
    print(buffer)
    val = [qk, sqlite3.Binary(buffer)]

    c.execute("INSERT INTO tiles(qk, data) VALUES (?,?)",val)

    conn.commit()
    print("Records created successfully")
    conn.close()
    pass

def create_db(dbPath):
    """

    :param dbPath:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("创建db成功" + dbPath)
    conn.close()
    _create_table(dbPath)
    pass

def _create_table(dbPath):
    """

    :param dbPath:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE tiles
           (qk text PRIMARY KEY     NOT NULL,
           data         BLOB);''')
    print("Table created successfully")
    conn.commit()
    conn.close()
    pass

def save_images(dbPath, qk):
    """
    显示图片
    :param dbPath:
    :param qk:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute("select data from tiles where qk="+ qk)

    for row in cursor:
        data = row[0]
        with open('test.jpg', 'wb') as out_file:
            out_file.write(data)

    conn.close()


