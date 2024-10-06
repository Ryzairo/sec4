from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, session, jsonify

import datetime
import os
import sqlite3
from sqlite3 import Row
from functools import wraps

app = Flask(__name__)
app.secret_key = 'DITISEENSECRETKEY123456789'



@app.route('/')
def index():
    conn = sqlite3.connect('WebAccess/Database/WebAccess.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    

    cursor.execute("SELECT * FROM Onderzoek WHERE Status = 'nieuw'")
    onderzoeksaanvragen = cursor.fetchall()

    conn.close()
    
    print([dict(x) for x in onderzoeksaanvragen])

    return render_template('dashboard.html', onderzoeksaanvragen=onderzoeksaanvragen)


@app.route('/api/goedkeuren/onderzoeksaanvragen')
def goedkeuren_onderzoeksaanvragen():
    conn = sqlite3.connect('WebAccess/Database/WebAccess.db')
    
    cursor = conn.cursor()

   
    cursor.execute("SELECT * FROM Onderzoek WHERE Status = 'nieuw'")
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000,debug = True)



