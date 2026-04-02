from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return jsonify({'message': '회원가입 성공!'})
    except:
        return jsonify({'message': '이미 존재하는 아이디입니다.'}), 400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return jsonify({'message': '로그인 성공!', 'redirect': '/profile'})
    else:
        return jsonify({'message': '아이디 또는 비밀번호가 틀렸습니다.'}), 401

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('hello'))
    return render_template('profile.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('hello'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)