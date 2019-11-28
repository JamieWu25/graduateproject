import requests
import random
import pymysql
from bs4 import BeautifulSoup
import time
import pdfplumber
import datetime
import re
import chardet
import random
import time
import rich
import fitz
import sys


def update(i):
    Today=datetime.date.today()
    ty=Today.year
    tm=Today.month
    td=Today.day

    db = pymysql.connect("203.64.84.94", "Fish", "851217", "project105")
    cur = db.cursor()


    sqlid="SELECT * FROM disease_t  ORDER BY id DESC LIMIT 0 , 1"

    try:
        cur.execute(sqlid)
        endid=cur.fetchall()
        endid=endid[0][0]
    except:
        db.rollback()

    for i in range (0,endid+1):

        sqlnew="SELECT date FROM disease_t WHERE id='%d'"%(i)
        #print(sqlnew)
        try:
            cur.execute(sqlnew)
            res = cur.fetchall()
            u = res[0][0]
            db.commit()
            print(u)
            if u!=None:
                u="".join(u)
                ii=u[4]
                if ii=="年":
                    tyy=int(u[0:4])
                    ss=u[5:7]
                    a = re.findall(r"([0-9]+)",ss)
                    str2="".join(a)
                    tmm=int(str2)
                    print(tyy)
                    print(tmm)
                    Score=(ty-tyy)*12-(tmm-tm)
                    if Score>120:
                        y=0*10
                    elif Score==0:
                        y=1*10
                    elif Score<=120:
                        y=(1-(((ty-tyy)*12-(tmm-tm))*0.00833))*10

                    print(y)
                    sql = "UPDATE disease_t SET timely = '%f' WHERE id = '%d'" % (y, i)
                    try:
                        cur.execute(sql)
                        db.commit()
                    except:
                        db.rollback()

            if u==None:
                y=0
                sql2 = "UPDATE disease_t SET timely = '%f' WHERE id = '%d'" % (y, i)
                try:
                    cur.execute(sql2)
                    db.commit()
                except:
                    db.rollback()

        except:
            db.rollback()

    db.close()
    print("Finsh")
    

if __name__=='__main__':
    print(sys.argv)
    update(sys.argv[0])











