##########################
### system level packages ###
##########################
import io
import os
import base64
import tempfile
import pickle
import requests
import random
import json

##########################
### 3rd party packages ###
##########################
from flask import Flask, render_template, request, redirect, url_for, session, current_app as app
from model import predict
from PIL import Image

app = Flask(__name__, static_folder="static")

# Generate a secure random key for session management
app.secret_key = os.urandom(24)  # Replace with your securely generated key

# Define a threshold for predictions
PREDICTION_THRESHOLD = 83.0  # Adjust this value based on your model's output

############# end of pages #################

##################################################
### Model prediction threshold is handled here ###
##################################################
# Why? you don't have to worry about it 🤡
def all_scores_below_threshold(predictions, threshold):
    """Check if all prediction scores are below the specified threshold."""
    return all(pred['score'] < threshold for pred in predictions)

#################
### Main page ###
#################

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

########################################################
### Classification demonstration with inputs example ###
########################################################

@app.route('/demo')
def demo():
    # Get the list of images from the static/images folder
    image_folder = os.path.join(app.static_folder, 'images')
    
    # Ensure the folder exists and contains files
    if not os.path.exists(image_folder):
        return "No image folder found", 500
    
    # List all image files
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))][:20]
    random.shuffle(image_files)

    # Ensure that image_files is not empty
    if not image_files:
        return "No images found in the static/images folder", 500
    
    # Pass image files to the template
    return render_template('demo.html', image_files=image_files)

######################################
### Displaying dataset information ###
######################################

@app.route('/dataset')
def dataset():
    # Load JSON data
    with open(os.path.join(app.static_folder, 'json', 'bark_items.json')) as f:
        data = json.load(f)
    return render_template('dataset.html', items=data['items'])
    
#################################################
### Predicting Image from the uploaded images ###
#################################################

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    image_file = request.files['file']
    
    if image_file.filename == '':
        return 'No file selected', 400

    # Process the uploaded image
    preview_image = Image.open(image_file).convert('RGB')
    
    predictions = predict(preview_image)

    data = io.BytesIO()
    preview_image.save(data, "JPEG")
    image_data = base64.b64encode(data.getvalue())

    if all_scores_below_threshold(predictions, PREDICTION_THRESHOLD):
        return render_template('error.html', image_data=image_data.decode('utf-8'))

    return render_template('result.html',
                           image_data=image_data.decode('utf-8'),
                           predictions=predictions)

################################################
###    Predicting Image from the given URL   ###
################################################

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

    if all_scores_below_threshold(predictions, PREDICTION_THRESHOLD):
        return render_template('error.html', image_data=image_data.decode('utf-8'))

    return render_template('result.html',
                           image_data=image_data.decode('utf-8'),
                           predictions=predictions)


################################################
### Predicting Image from the example images ###
################################################

@app.route('/predict/<image_name>', methods=['POST'])
def predict_image(image_name):
    image_path = os.path.join(app.static_folder, 'images', image_name)
    
    if not os.path.exists(image_path):
        return "Image not found", 404

    preview_image = Image.open(image_path).convert('RGB')
    predictions = predict(preview_image)

    data = io.BytesIO()
    preview_image.save(data, "JPEG")
    image_data = base64.b64encode(data.getvalue())

    if all_scores_below_threshold(predictions, PREDICTION_THRESHOLD):
        return render_template('error.html', image_data=image_data.decode('utf-8'))

    # Store data in a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
    with open(temp_file.name, 'wb') as f:
        pickle.dump({'predictions': predictions, 'image_data': image_data.decode('utf-8')}, f)

    # Store the temp file path in the session
    session['temp_file'] = temp_file.name

    return redirect(url_for('result_page'))


@app.route('/result')
def result_page():
    temp_file_path = session.pop('temp_file', None)
    if temp_file_path and os.path.exists(temp_file_path):
        with open(temp_file_path, 'rb') as f:
            data = pickle.load(f)
        
        predictions = data.get('predictions', [])
        image_data = data.get('image_data', '')

        os.remove(temp_file_path)  # Clean up the temporary file

        return render_template('result.html', image_data=image_data, predictions=predictions)
    else:
        return "No result found", 404
    
#######################################################
### END of Predicting Image from the example images ###
#######################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)