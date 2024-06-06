from flask import Flask, render_template, request, redirect, url_for
import requests
import mysql.connector
import re
from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        user="ganesh",
        password="microsoft@123",
        host="loginfrt-mysql-server123.mysql.database.azure.com",
        port=3306,
        database="your_database_name",
        ssl_ca=r'C:\Certificates\DigiCertGlobalRootG2.crt.pem',
        ssl_disabled=False
    )
@app.route('/connect.html')
def connect():
    return render_template('connect.html')

@app.route('/')
def home():
    return render_template('first.html')

@app.route('/index.html')
def index():
    return render_template('index.html') 

@app.route('/about.html')
def page1():
    return render_template('about.html')

@app.route('/coding.html')
def page2():
    return render_template('coding.html')


@app.route('/commu.html')
def page3():
    return render_template('commu.html')

@app.route('/maths.html')
def page4():
    return render_template('maths.html')

@app.route('/resource.html')
def page5():
    return render_template('resource.html')

@app.route('/road.html')
def page6():
    return render_template('road.html')

@app.route('/web.html')
def page7():
    return render_template('web.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    account = cursor.fetchone()
    cursor.close()
    conn.close()
    if account:
        return redirect(url_for('connect'))  
    else:
        return 'Incorrect email/password!'

# Route for signup
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account:
        cursor.close()
        conn.close()
        return 'Account already exists!'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        cursor.close()
        conn.close()
        return 'Invalid email address!'
    elif not email or not password:
        cursor.close()
        conn.close()
        return 'Please fill out the form!'
    else:
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('connect'))  


@app.route("/jobs")
def hello_jovian():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  
  if not job:
    return "Not Found", 404
  
  return render_template('jobpage.html', job=job)

@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)

@app.route("/job/<id>/apply", methods=['POST'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html', 
                         application=data,
                         job=job)

subscription_key = "9cafdf6e008e45199cf44beb904c9daf"  # Your actual subscription key
endpoint = "https://api.cognitive.microsofttranslator.com/translate"  # Your specific endpoint

@app.route('/language')
def lang():
    return render_template('translate.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = request.form['lang']
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'centralindia',  # Your region
        'Content-type': 'application/json'
    }
    params = {
        'api-version': '3.0',
        'to': target_lang
    }
    body = [{
        'text': text
    }]
    response = requests.post(endpoint, params=params, headers=headers, json=body)
    if response.status_code == 200:
        translation = response.json()[0]['translations'][0]['text']
        return jsonify({'translation': translation})
    else:
        return jsonify({'error': 'Translation failed'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
