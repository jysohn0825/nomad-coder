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
    session['username'] = name
    return redirect(url_for('friends'))
    # conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    # cur = conn.cursor()

    # try:
    #     sql = "Select * from user where USER_ID = '" + name + "'"
    #     cur.execute(sql)
    #     userinfo = cur.fetchone()
    #     if name == '' or None :
    #         return redirect(url_for('index'))
    #     elif userinfo[2] == pwd:
    #         session['username'] = name
    #         return redirect(url_for('friends'))
    #     else:
    #         return redirect(url_for('index'))
    # except:
    #     return redirect(url_for('index'))
    # finally:
    #     cur.close()
    #     conn.close()


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

    # conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    # cur = conn.cursor()

    # try:
    #     sql = "Select * from user where USER_ID = '" + name + "'"
    #     cur.execute(sql)
    #     userinfo = cur.fetchone()
    #     if name == '' or None :
    #         return redirect(url_for('index'))
    #     elif userinfo[2] == pwd:
    #         session['username'] = name
    #         return redirect(url_for('friends'))
    #     else:
    #         return redirect(url_for('index'))
    # except:
    #     return redirect(url_for('index'))
    # finally:
    #     cur.close()
    #     conn.close()



@app.route('/logout')
def logout() :
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/friends')
def friends() :
    username = session['username']
    return render_template('/friends.html', username = username)

@app.route('/profile', methods=['GET'])
def profile() :
    username = session['username']
    return render_template('/profile.html',username = username)

@app.route('/image', methods=['GET'])
def image() :
    username = session['username']
    return render_template('/image.html',username = username)

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
    return render_template('/more.html',username = username)

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