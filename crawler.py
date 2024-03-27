import requests as req
import os
from os.path import abspath
from bs4 import BeautifulSoup as bs
import pymysql

host = 'project-db-cgi.smhrd.com'
port = 3307
user = 'cgi_23K_AI3_mini_1'
password = 'smhrd1'
dbName = 'cgi_23K_AI3_mini_1'

conn = pymysql.connect(host=host, port=port, user=user, password=password, db=dbName, charset='utf8')
cur=conn.cursor()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

category = ['0401','0402','0403','0404','0405','0408','0409']

sql_rows = []

try:
    for cate in category:

        for pageNo in range(1,2):
            url = 'https://www.hankyung.com/economy/{}?page={}'.format(cate, pageNo)

            res = req.get(url, headers = headers)
            html = bs(res.content, 'lxml')

            tit_tags = html.select('h3.tit > a')

            for tit in tit_tags: 
                title = tit.text.replace('"','')
                sql_row = '({})'.format('"'+title+'"')
                sql_rows.append(sql_row)

    if sql_rows:
        sql = 'INSERT INTO test(data) VALUES ' + ','.join(sql_rows)
        cur.execute(sql)

        conn.commit()
        conn.close() 
except:
    conn.close() 

print('수집완료!')
