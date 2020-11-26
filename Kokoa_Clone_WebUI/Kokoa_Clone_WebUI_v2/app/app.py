import pymysql
import datetime
from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = 'any random string'

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
        sql = "SELECT * FROM USER WHERE USER_ID = '" + name + "'"
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
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "INSERT USER VALUES('" + id + "', '" + name + "', '" + pwd + ", null, null, null, '" + email + "')"
    cur.execute()
    conn.commit()
    session['username'] = id
    cur.close()
    conn.close()
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
    sql = "SELECT * FROM USER WHERE USER_ID IN (SELECT USER2 FROM FRIENDS WHERE USER1 = '" + username + "')"
    sql+= " UNION "
    sql+= "SELECT * FROM USER WHERE USER_ID IN (SELECT USER1 FROM FRIENDS WHERE USER2 = '" + username + "')"
    cur.execute(sql)
    fList = list(cur.fetchall())
    fList.sort()
    sql = "SELECT * FROM USER WHERE USER_ID = '" + username + "'"
    cur.execute(sql)
    my = cur.fetchone()

    sql = "SELECT COUNT(CASE WHEN CHAT_FLAG = 1 THEN 1 END)"
    sql+= "FROM CHAT WHERE CHAT.USER_ID != '"+username+"'"
    cur.execute(sql)
    count = cur.fetchone()[0]

    cur.close()
    conn.close()
    return render_template('/friends.html', my = my, fList = fList, count = count)

@app.route('/changeProfile', methods=['POST'])
def changeProfile():
    username = session['username']
    name = request.form['username']
    comment = request.form['comment']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "UPDATE USER SET USER_NAME = '" + name + "', USER_SELF = '" + comment + "' WHERE USER_ID = '" + username + "'"
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
    sql = "SELECT * FROM USER WHERE USER_ID = '" + user + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/profile.html',username = username, userProfile = userProfile)

@app.route('/profile/<user>/image', methods=['GET'])
def image(user) :
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM USER WHERE USER_ID = '" + user + "'"
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
    sql = "SELECT * FROM USER WHERE USER_ID = '" + user + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/edit.html', userProfile = userProfile)

@app.route('/chats', methods=['GET'])
def chats() :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT CR.ROOM, CR.USER, USER.USER_NAME, CR.NONREAD, CR.LATEST, USER.USER_PIC "
    sql+= "FROM USER, (SELECT CHATROOM.ROOM_ID AS ROOM, CASE  WHEN USER1 = '"+username+"' THEN USER2 ELSE USER1 END AS USER, "
    sql+= "COUNT(CASE WHEN CHAT_FLAG = 1 AND USER_ID != '"+username+"' THEN 1 END) AS NONREAD, MAX(SUBSTRING(CHAT_TIME,1,16)) AS LATEST "
    sql+= "FROM CHAT, CHATROOM "
    sql+= "WHERE CHATROOM.ROOM_ID = 1) AS CR "
    sql+= "WHERE CR.USER = USER.USER_ID"
    cur.execute(sql)
    rList = list(cur.fetchall())
    rList.sort()

    sql = "SELECT COUNT(CASE WHEN CHAT_FLAG = 1 THEN 1 END)"
    sql+= "FROM CHAT WHERE CHAT.USER_ID != '"+username+"'"
    cur.execute(sql)
    count = cur.fetchone()[0]

    cur.close()
    conn.close()
    return render_template('/chats.html', rList = rList, count = count)

@app.route('/findRoom/<userID>', methods = ['GET'])
def findRoom(userID):
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT ROOM_ID FROM CHATROOM "
    sql+= "WHERE (USER1 = '"+userID+"' AND USER2 = '"+username+"') OR (USER1 = '"+username+"' AND USER2 = '"+userID+"')"
    cur.execute(sql)
    temp = cur.fetchone()
    if temp is None:
        sql = "INSERT INTO CHATROOM (USER1, USER2) values ('"+username+"', '"+userID+"');"
        cur.execute(sql)
        conn.commit()
        sql = "SELECT ROOM_ID FROM CHATROOM "
        sql += "WHERE (USER1 = '" + userID + "' AND USER2 = '" + username + "') OR (USER1 = '" + username + "' AND USER2 = '" + userID + "')"
        cur.execute(sql)
        chatnum = str(cur.fetchone()[0])
        pass
    else:
        chatnum = str(temp[0])
    cur.close()
    conn.close()
    return redirect("/../chat/" + chatnum)

@app.route('/chat/<chatnum>/send', methods=['POST'])
def chatSend(chatnum):
    username = session['username']
    message = request.form['send']

    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "INSERT INTO CHAT VALUES (null,'"+nowDatetime+"','"+ username + "','"+message+"',"+str(chatnum)+",1)"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return redirect("../../chat/"+chatnum)

@app.route('/chat/<chatnum>/read', methods=['GET'])
def readChat(chatnum):
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "UPDATE CHAT SET CHAT_FLAG = 0 WHERE USER_ID != '"+username+"' AND ROOM_ID = "+chatnum
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return redirect("../../chat/"+chatnum)

@app.route('/chat/<chatnum>', methods=['GET'])
def chat(chatnum) :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT CHAT.USER_ID, USER_NAME, CHAT_LOG, SUBSTRING(CHAT_TIME,11,6), USER_PIC "
    sql+= "FROM CHAT, USER "
    sql+= "WHERE ROOM_ID = '"+chatnum+"' AND USER.USER_ID = CHAT.USER_ID "
    sql+= "ORDER BY CHAT_TIME"
    cur.execute(sql)
    cList = list(cur.fetchall())
    sql = "SELECT * FROM CHATROOM "
    sql+= "WHERE (USER1 = '"+ username + "' OR USER2 = '"+ username + "') AND ROOM_ID = "+chatnum
    cur.execute(sql)
    rName = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('/chat.html', username = username, chatnum = chatnum, cList = cList, rName = rName)

@app.route('/find', methods=['GET'])
def fin() :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT COUNT(CASE WHEN CHAT_FLAG = 1 THEN 1 END)"
    sql+= "FROM CHAT WHERE CHAT.USER_ID != '"+username+"'"
    cur.execute(sql)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template('/find.html', count = count)

@app.route('/more', methods=['GET'])
def mor() :
    username = session['username']
    conn = pymysql.connect(host=IP, user=USER, password=PASSWORD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM USER WHERE USER_ID = '" + username + "'"
    cur.execute(sql)
    userProfile = cur.fetchone()
    sql = "SELECT COUNT(CASE WHEN CHAT_FLAG = 1 THEN 1 END)"
    sql+= "FROM CHAT WHERE CHAT.USER_ID != '"+username+"'"
    cur.execute(sql)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template('/more.html',userProfile = userProfile, count = count)

@app.route('/settings', methods=['GET'])
def set() :
    return render_template('/settings.html')


# DB 관련
conn, cur = None, None
IP = '127.0.0.1'
USER = 'root'
PASSWORD = '4321'
DB = 'Kokoa'
fileList = None

if __name__ == '__main__' :
    app.run(host='127.0.0.1', port='30')