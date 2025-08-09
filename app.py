import cv2
from keras.models import load_model
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import base64
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash,
check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key_here'

# Load FER model
model = load_model("fer.h5")

# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# DB Initialization
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emotion TEXT,
            timestamp DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Image preprocessing
def extract_features(image):
    image = np.array(image).reshape(1, 48, 48, 1) / 255.0
    return image


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page.")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


# -------- Routes -------- #
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        session['username'] = username
        return redirect(url_for('home'))
    else:
        flash('Invalid login')
        return redirect(url_for('login_page'))
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Account created. Please login.')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('main.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/demo')
@login_required
def demo():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('demo.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'user_id' not in session:
        return jsonify({'success': False, 'emotion': 'Unauthorized'})

    data = request.get_json()
    img_data = base64.b64decode(data['image'])
    npimg = np.frombuffer(img_data, dtype=np.uint8)
    im = cv2.imdecode(npimg, 1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    response = {'success': False}
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48, 48))
            img = extract_features(face)
            pred = model.predict(img)
            predicted_emotion = labels[pred.argmax()]
            
            # Save to DB
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO emotions (user_id, emotion, timestamp) VALUES (?, ?, ?)",
                      (session['user_id'], predicted_emotion, datetime.now()))
            conn.commit()
            conn.close()

            response = {'emotion': predicted_emotion, 'success': True}
            break
    else:
        response['emotion'] = 'No face detected'

    return jsonify(response)

@app.route('/report')
@login_required
def report():
    if 'user_id' not in session:
        flash("Login required to view report.")
        return redirect(url_for('login'))

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Get count of each emotion
    c.execute('SELECT emotion, COUNT(*) FROM emotions WHERE user_id=? GROUP BY emotion', (session['user_id'],))
    summary_rows = c.fetchall()

    emotion_counts = {label: 0 for label in labels}
    for emotion, count in summary_rows:
        emotion_counts[emotion] = count

    # Get timeline of emotions with timestamps
    c.execute('SELECT timestamp, emotion FROM emotions WHERE user_id=? ORDER BY timestamp ASC', (session['user_id'],))
    timeline_rows = c.fetchall()
    emotion_timings = [(ts, emo) for ts, emo in timeline_rows]

    conn.close()

    return render_template(
        'report.html',
        emotion_counts=emotion_counts,
        emotion_timings=emotion_timings,
        username=session['username']
    )

if __name__ == "__main__":
    app.run(debug=True)
