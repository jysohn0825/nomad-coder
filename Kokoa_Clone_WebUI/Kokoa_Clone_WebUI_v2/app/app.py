import requests
import pymysql
from flask import Flask, render_template, jsonify, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = 'any random string'

## HTML을 주는 부분
@app.route('/')
def index() :
    if 'username' in session :
        if 'username' != '' or None :
            return redirect(url_for('friends'))
        else :
            session.pop('username', None)
            return redirect(url_for('index'))
    return render_template('/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login() :
    name = request.form['username']
    pwd = request.form['password']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    try:
        sql = "Select * from user where USER_ID = '" + name + "'"
        cur.execute(sql)
        userinfo = cur.fetchone()
        if name == '' or None :
            return redirect(url_for('index'))
        elif userinfo[2] == pwd:
            session['username'] = name
            return redirect(url_for('friends'))
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))
    finally:
        cur.close()
        conn.close()

@app.route('/sign', methods=['POST'])
def sign() :
    return render_template('/sign.html')

@app.route('/signup', methods=['POST'])
def signup() :
    name = request.form['name']
    id = request.form['username']
    pwd = request.form['password']
    email = request.form['email']
    print(name, id, pwd, email)
    session['username'] = id
    return redirect(url_for('friends'))

@app.route('/logout')
def logout() :
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/friends')
def friends() :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE USER_ID IN (SELECT USER2 FROM friends WHERE USER1 = '" + username + "')"
    sql+= " UNION "
    sql+= "SELECT * FROM user WHERE USER_ID IN (SELECT USER1 FROM friends WHERE USER2 = '" + username + "')"
    cur.execute(sql)
    fList = list(cur.fetchall())
    fList.sort()
    sql = "SELECT * FROM user WHERE USER_ID = '" + username + "'"
    cur.execute(sql)
    my = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/friends.html', my = my, fList = fList)

@app.route('/changeProfile', methods=['POST'])
def changeProfile():
    username = session['username']
    name = request.form['username']
    comment = request.form['comment']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "UPDATE user SET USER_NAME = '" + name + "', USER_SELF = '" + comment + "' WHERE USER_ID = '" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return redirect("profile/"+username)

@app.route('/profile/<user>', methods=['GET'])
def profile(user) :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE USER_ID = '" + user + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/profile.html',username = username, userProfile = userProfile)

@app.route('/profile/<user>/image', methods=['GET'])
def image(user) :
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE USER_ID = '" + user + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/image.html',userProfile = userProfile)


@app.route('/profile/<user>/edit')
def edit(user) :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE USER_ID = '" + user + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/edit.html', userProfile = userProfile)

@app.route('/chats', methods=['GET'])
def channel() :
    return render_template('/chats.html')

@app.route('/chat', methods=['GET'])
def ch1() :
    return render_template('/chat.html')

@app.route('/find', methods=['GET'])
def fin() :
    return render_template('/find.html')

@app.route('/more', methods=['GET'])
def mor() :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM user WHERE USER_ID = '" + username + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/more.html',userProfile = userProfile)

@app.route('/settings', methods=['GET'])
def set() :
    return render_template('/settings.html')

## 전역 변수부

# DB 관련
conn, cur = None, None
IP = '127.0.0.1'
USER = 'root'
PASSWORD = '4321'
DB = 'Kokoa'
fileList = None

if __name__ == '__main__' :
    app.run(host='127.0.0.1', port='30')