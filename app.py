from flask import Flask, render_template, request, redirect, url_for
from model import predict
from PIL import Image
import base64
import io
import requests

app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return 'No file selected', 400

    image_file = request.files['file']
    if image_file:
        preview_image = Image.open(image_file).convert('RGB')
        predictions = predict(preview_image)

        data = io.BytesIO()
        preview_image.save(data, "JPEG")
        image_data = base64.b64encode(data.getvalue())

        return render_template('result.html',
                               image_data=image_data.decode('utf-8'),
                               predictions=predictions)

@app.route('/process_url', methods=['POST'])
def process_url():
    image_url = request.form['image_url']
    if not image_url:
        return 'No URL provided', 400

    response = requests.get(image_url)
    if response.status_code != 200:
        return 'Failed to download image', 400

    image = Image.open(io.BytesIO(response.content)).convert('RGB')
    predictions = predict(image)

    data = io.BytesIO()
    image.save(data, "JPEG")
    image_data = base64.b64encode(data.getvalue())

    return render_template('result.html',
                           image_data=image_data.decode('utf-8'),
                           predictions=predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
