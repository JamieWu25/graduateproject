import requests

from bs4 import BeautifulSoup

import re

from langdetect import detect

import pymysql

import random

import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}


def getweb(url):
    htmlpage = requests.get(url, headers=headers)

    # print(htmlpage.ret)

    if htmlpage.status_code != 200:

        print(htmlpage.status_code)

    else:

        return htmlpage.text


def ree(u, gu):
    print(gu)

    db = pymysql.connect("203.64.84.94", "Fish", "851217", "project105")

    cur = db.cursor()

    # print(u)

    c3 = []

    c1 = u.split('，')

    for i in range(len(c1)):
        c2 = c1[i].split(' ')

        c3.extend(c2)

    c2 = []

    for i in range(len(c3)):
        c1 = c3[i].split('。')

        c2.extend(c1)

    c1 = []

    for i in range(len(c2)):
        c3 = c2[i].split('？')

        c1.extend(c3)

    c3 = []

    for i in range(len(c1)):
        c2 = c1[i].split('!')

        c3.extend(c2)

    c2 = []

    for i in range(len(c3)):
        c1 = c3[i].split('；')

        c2.extend(c1)

    co = 0

    row = 0

    k = 0

    cn = 0

    en = 0

    e = 0

    snum = 0

    scount = 0

    for z in range(len(c2)):

        c2[z] = c2[z].replace('\n', '')

        st = re.sub("[\s+\.\!\/_,$%^*()+\"\']+|[+——！★◎：X:《》【】，。？、～~@#￥%……&*（）「」]+", "", c2[z])

        co = co + len(st)

        if len(st) > 0:
            row = row + 1

        if st[0:1].isdigit():

            continue

        else:

            try:

                if detect(st[0:1]) == 'ko':

                    k = k + 1

                elif detect(st[0:1]) == 'zh-tw':

                    k = k + 1

                elif detect(st[0:1]) == 'zh-cn':

                    cn = cn + 1

                elif st[0:1].isalpha():

                    en = en + 1

                else:

                    e = e + 1

            except:

                continue

        for j in range(len(st) - 1):

            print(st[j:j + 2])

            if st[j + 1:j + 2].isdigit():

                continue

            else:

                try:

                    if detect(st[j + 1:j + 2]) == 'ko':

                        k = k + 1

                    elif detect(st[j + 1:j + 2]) == 'zh-tw':

                        k = k + 1

                    elif detect(st[j + 1:j + 2]) == 'zh-cn':

                        cn = cn + 1

                    elif st[j + 1:j + 2].isalpha():

                        en = en + 1

                    else:

                        e = e + 1

                except:

                    continue

            if st[j:j + 1].encode('UTF-8').isalpha() or st[j + 1:j + 2].encode('UTF-8').isalpha():

                continue

            else:

                sql2 = " SELECT value FROM googlesearch_t WHERE name='%s'" % (st[j:j + 2])

                try:

                    cur.execute(sql2)

                    nu = cur.fetchall()

                    print(len(nu))

                    if len(nu) == 0:

                        key = '"' + st[j:j + 2] + '"'

                        res = "https://www.google.com.tw/search?q=" + key

                        html = getweb(res)

                        if html != None:

                            soup = BeautifulSoup(html, 'html.parser')

                            st1 = soup.find("div", id="resultStats")

                            a = st1.text.find("項")

                            st2 = st1.text[3:a]

                            st2 = st2.replace(",", "")

                            n3 = int(st2)

                            sql3 = "INSERT INTO googlesearch_t(name,value) VALUES ('%s','%d')" % (st[j:j + 2], n3)

                            try:

                                cur.execute(sql3)

                                db.commit()

                            except:

                                db.rollback()

                        t = random.randint(20, 50)

                        time.sleep(t)

                    else:

                        # print(nu[0][0])

                        n3 = int(nu[0][0])

                    print(n3)

                    if n3 >= 100000000:

                        x3 = 1

                    elif n3 <= 5000000:

                        x3 = 0

                    else:

                        x3 = (n3 / 10000) / 9500 - 0.0526315789

                    snum = snum + x3

                    scount = 1 + scount

                except:

                    db.rollback()

    avg = co / row

    if avg >= 26.31:

        y1 = 0

    elif avg <= 9.77:

        y1 = 1

    else:

        y1 = -0.057 * avg + 1.5

    x2 = 0.35 * (en / co) + 0.15 * (cn / co) + 0.5 * (e / co)

    y2 = -2 * x2 + 1

    y3 = snum / scount

    # print("一句字長",y1,"\n語言",y2,"\n專有名詞",y3)

    a1 = (0.2 * y1 + 0.45 * y2 + 0.35 * y3) * 10

    print(gu, a1)

    nea=(a1-5.25)/2.3
    if nea>1:
        nea=1
    elif nea<0:
        nea=0 
    sql4 = "UPDATE disease_t SET readable = '%f',norreadable='%f' WHERE id = '%d'" % (a1,nea*10, gu)

    try:

        cur.execute(sql4)

        db.commit()

    except:

        db.rollback()

    db.close()

