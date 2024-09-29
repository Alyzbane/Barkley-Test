# TODO:
# Add confidence level
# Add  oob
# Add unknown clas (ImageNet?)

from transformers import AutoModelForImageClassification, AutoImageProcessor, pipeline
import os
import torch
import numpy as np

repo_name = "model/FBark_1k_2e-5"
device = torch.device('cuda' if torch.cuda.is_available() else "cpu")

if not os.path.exists(repo_name):
    repo_name = "alyzbane/resnet-50-finetuned-FBark-1k"

model = AutoModelForImageClassification.from_pretrained(repo_name).to(device)
image_processor = AutoImageProcessor.from_pretrained(repo_name)

pipe = pipeline("image-classification", model=model, feature_extractor=image_processor, device=device)

# ======= Boundary for confidence level ==========
LOW_SCORE_LIMIT=50.0

# ======= Boundary for confidence level ==========

# Dictionary mapping scientific names to common names
name_mapping = {
    "Roystonea regia": "Royal Palm",
    "Pterocarpus indicus": "Narra",
    "Tabebuia": "Trumpet Tree",
    "Mangifera indica": "Mango Tree",
    "Iinstia bijuga": "Ipil Tree"
}

def predict(image):
    predictions = pipe(image)
    for prediction in predictions:
        prediction['score'] = round(prediction['score'] * 100, 3)  # limiting to 3 decimal places
        scientific_name = prediction['label']
        common_name = name_mapping.get(scientific_name, "Unknown")
        prediction['scientific_name'] = scientific_name
        prediction['common_name'] = common_name

    return predictions  # return the predictions with scientific and common names
