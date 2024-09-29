import csv
import os
from num2words import num2words as n2w

def create_csv_with_dynamic_images(image_folder, output_csv_path=r'../static/csv/dataset.csv'):
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # List all image files from the folder (just filenames + extension)
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Prepare data for the CSV file
    data = []
    for idx, image in enumerate(images, start=1):
        numword = n2w(f'{idx}', )  # Convert the number to words
        # Only use the filename with extension
        image_path = f'images/{image}'
        data.append({
            'id': idx,
            'image': image_path,  # Add the 'static/images/' path prefix
            'text': f'Text for section {idx}.'
        })

    # Create the CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'image', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for row in data:
            writer.writerow(row)

    print(f"CSV file created at {output_csv_path}")

# Example usage
create_csv_with_dynamic_images('../static/images')
