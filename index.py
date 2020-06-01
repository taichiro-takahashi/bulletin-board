#!/usr/bin/env python3
# coding: utf-8

import cgitb; cgitb.enable()
import cgi
import datetime
import MySQLdb
import sys
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

read_default = config_ini['DEFAULT']
user = read_default.get('User')

read_default = config_ini['DEFAULT']
password = read_default.get('Password')

con = None
cur = None

print("Content-type: text/html; charset=utf-8")

print(
"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="css/style.css">
<title>ひと言掲示板</title>
</head>

<body>
<h1>ひと言掲示板</h1>
<form method="post" action="index.py">
        <div>
                <label for="name">表示名</label>
                <input id="name" type="text" name="name" value="">
        </div>
        <div>
                <label for="message">ひと言メッセージ</label>
                <textarea id="message" name="message"></textarea>
        </div>
        <input type="submit" name="btn_submit" value="書き込む">
</form>
<hr>
<section>
"""
)

def message():
    """ 接続サンプル """
    # 接続する
    con = MySQLdb.connect(
            user=user,
            passwd=password,
            host='localhost',
            db='bbs_db',
            charset="utf8")
    # カーソルを取得する
    cur= con.cursor()
    # クエリを実行する
    sql = "select *  from message_list order by id desc"
    cur.execute(sql)
    # 実行結果をすべて取得する
    rows = cur.fetchall()

    for row in rows:
        source = ( '''
        <article>
            <div class="info">
                <h2>{name}</h2>
                <time>{date}</time>
            </div>
            <p>{text}</p>
        </article>
        ''').format( name = row[1],
            text = row[2],
            date = row[3]
            )
        print(source)

    cur.close()
    con.close()
if __name__ == "__main__":
    message()

print(
"""
</section>
</body>
</html>
"""
)

form = cgi.FieldStorage()

print("")

if "message" not in form:
    sys.exit()

veiw_name = form.getvalue("name")
veiw_text = form.getvalue("message")

def bbs():
    """ 接続サンプル """
    # 接続する
    con = MySQLdb.connect(
            user=user,
            passwd=password,
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
    <meta http-equiv="refresh" content="0;URL=index.py">
  </head>
</html>
"""
)
