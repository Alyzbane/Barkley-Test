from transformers import AutoModelForImageClassification, AutoImageProcessor, pipeline
import torch

# repo_name = "model/new/ConvNeXT"
repo_name = "model/ResNet-50"
repo_name = "model/new/Swin-base-patch4-window7"
# repo_name = "model/new/ViT-base-patch16"

device = torch.device('cuda' if torch.cuda.is_available() else "cpu")

model = AutoModelForImageClassification.from_pretrained(repo_name).to(device)
image_processor = AutoImageProcessor.from_pretrained(repo_name)
pipe = pipeline("image-classification", model=model, feature_extractor=image_processor, device=device)

# Dictionary mapping scientific names to common names
name_mapping = {
    "Roystonea regia": "Royal Palm",
    "Pterocarpus indicus": "Narra",
    "Tabebuia": "Trumpet Tree",
    "Mangifera indica": "Mango Tree",
    "Iinstia bijuga": "Ilang-ilang Tree"
}

def predict(image):
    predictions = pipe(image)
    for prediction in predictions:
        prediction['score'] = round(prediction['score'] * 100, 3)  # limiting to 3 decimal places
        scientific_name = prediction['label']
        
        # Update scientific name display
        if scientific_name == "Iinstia bijuga":
            scientific_name = "Cananga odorata"
        
        # Get the common name from the mapping
        common_name = name_mapping.get(prediction['label'], "Unknown")
        
        # Update the prediction dictionary
        prediction['scientific_name'] = scientific_name
        prediction['common_name'] = common_name

    return predictions

