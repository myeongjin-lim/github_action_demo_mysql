import requests as req
import time
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

sql_rows = []

try:

    url = 'https://news.naver.com/breakingnews/section/105/230'

    res = req.get(url, headers = headers)
    html = bs(res.content, 'lxml')

    news_a_tag = html.select('a.sa_text_title')

    for a in news_a_tag: 
    #     print(tit.text)
        title = a.text.replace('"','').replace('\n','')
        sql_row = '({})'.format('"'+title+'"')
        sql_rows.append(sql_row)

#         time.sleep(1)

    if sql_rows:
        sql = 'INSERT INTO test(data) VALUES ' + ','.join(sql_rows)
        cur.execute(sql)

        conn.commit()
        conn.close() 
except Exception as e:
    print('오류발생', e)
    conn.close() 

print('수집완료!')
