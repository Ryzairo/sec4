from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'geheim'  
app.database = "testgpt.db"  

@app.route('/main')
def index():
    # Connect to db file "testgpt.db"
    try:
        conn = sqlite3.connect('testgpt.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM teachers')
        data = cursor.fetchall()
        conn.close()

        if 'username' in session:
            return render_template('index.html', data=data, username=session['username'])
        else:
            return redirect(url_for('login'))

    except Exception as e:
        # Log the error and return an error page
        app.logger.error(f"Error: {e}")
        return render_template('error.html', error_message="An error occurred while fetching data.")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def connect_db():
    return sqlite3.connect(app.database)

def check_credentials(username, password):
    db = connect_db()
    cursor = db.execute('SELECT * FROM teachers WHERE username=? AND teacher_password=?', (username, password))
    user = cursor.fetchone()
    db.close()
    return user is not None

if __name__ == '__main__':
    app.run(debug=True)