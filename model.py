from transformers import AutoModelForImageClassification, AutoImageProcessor, pipeline
import os

model_checkpoint = r"microsoft/resnet-50"
model_name = model_checkpoint.split("/")[-1]
repo_name = "model/resnet-50-finetuned-FBark-1k"

if not os.path.exists(repo_name):
    repo_name = "alyzbane/resnet-50-finetuned-FBark-1k"
    
model = AutoModelForImageClassification.from_pretrained(repo_name)
image_processor = AutoImageProcessor.from_pretrained(repo_name)
pipe = pipeline("image-classification", model=model, feature_extractor=image_processor)

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
