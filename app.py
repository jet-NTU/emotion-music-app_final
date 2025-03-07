
import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': '未提供圖片'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': '未選擇檔案'}), 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    try:
        result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        return jsonify({'emotion': emotion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("static/" + path):
        return send_from_directory("static", path)
    else:
        return send_from_directory("static", "index.html")

if __name__ == '__main__':
    app.run(debug=True)
