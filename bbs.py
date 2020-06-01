#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import cgi
import cgitb
import MySQLdb
import sys
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

read_default = config_ini['DEFAULT']
user = read_default.get('User')

read_default = config_ini['DEFAULT']
pass = read_default.get('Password')

con = None
cur = None
cgitb.enable()

form = cgi.FieldStorage()

print("Content-Type: text/html; charset=UTF-8")
print("")

if "message" not in form:
    print("<h1>テキストが空白です</h1>")
    print("<br>")
    print("テキストを入力してください！")
    print("<a href='index.py'><button type='submit'>戻る</button></a>")
    sys.exit()

veiw_name = form.getvalue("name")
veiw_text = form.getvalue("message")

def bbs():
    """ 接続サンプル """
    # 接続する
    con = MySQLdb.connect(
            user=user,
            passwd=pass,
            host='localhost',
            db='bbs_db',
            charset="utf8")
    # カーソルを取得する
    cur= con.cursor()
    # クエリを実行する
    sql = "INSERT INTO message_list (name, text) values (%s, %s)"
    cur.execute(sql,(veiw_name, veiw_text))
    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    bbs()

print(
"""
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="3;URL=index.py">
  </head>
  <body>
    <p>書き込みが完了しました。</p>
    <p>3秒後、元のページに戻ります。</p>
  </body>
</html>
"""
)
