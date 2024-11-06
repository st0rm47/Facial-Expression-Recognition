import cv2
from keras.models import load_model
import numpy as np
from flask import Flask, request, jsonify, render_template
import base64

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')   

# Load the emotion detection model
model = load_model("fer.h5")

# Haar cascade for face detection
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# Labels for emotion prediction
labels = {0: 'Angry', 
          1: 'Disgust', 
          2: 'Fear', 
          3: 'Happy', 
          4: 'Neutral', 
          5: 'Sad', 
          6: 'Surprise'}

# Function to extract features
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Route to render the main page
@app.route('/')
def index():
    return render_template('main.html')

# Route to render demo page
@app.route('/demo')
def demo():
    return render_template('demo.html')

# Route to handle webcam feed and process emotion
@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    img_data = base64.b64decode(data['image'])
    npimg = np.frombuffer(img_data, dtype=np.uint8)
    im = cv2.imdecode(npimg, 1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    response = {'success': False}
    if len(faces) > 0:
        for (p, q, r, s) in faces:
            face_img = gray[q:q + s, p:p + r]
            face_img = cv2.resize(face_img, (48, 48))
            img = extract_features(face_img)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]
            response = {'emotion': prediction_label, 'success': True}
            break
    else:
        response['emotion'] = 'No face detected'

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
