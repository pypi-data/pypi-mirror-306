import requests
import os

def fetch_images(condition=None, stage=None, count=1):
    # Map conditions and stages to categories
    category_map = {
        "normal_lung": "normal_lung_ct",
        "lung_cancer": "lung_cancer_ct",
        # "alzheimer": {
        #     "non-demented": "alzheimer-non-demented",
        #     "mild": "alzheimer-mild",
        #     "very-mild": "alzheimer-very-mild",
        #     "moderate": "alzheimer-moderate"
        
    }
    
    # Determine the category based on the condition and stage
    if condition == "lung_cancer":
        category = category_map["lung_cancer"]
    elif condition == "normal_lung":
        category = category_map["normal_lung"]
    elif condition == "alzheimer" and stage in category_map["alzheimer"]:
        category = category_map["alzheimer"][stage]
    else:
        raise ValueError("Invalid condition or stage")

    # Make API request to get images
    response = requests.get('https://localhost:5000/', params={'category': category, 'num': count})

    if response.status_code != 200:
        raise Exception("Failed to fetch images: " + response.json().get("error", "Unknown error"))

    image_urls = response.json().get("images", [])
    
    # Create a separate download directory for the category
    download_dir = os.path.join('images', category)  # This will create a path like 'images/lung_cancer_ct'
    os.makedirs(download_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Download the images
    downloaded_images = []
    for image_url in image_urls:
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            # Save the image
            img_name = os.path.join(download_dir, os.path.basename(image_url))
            with open(img_name, 'wb') as f:
                f.write(img_response.content)
            downloaded_images.append(img_name)
        else:
            print(f"Failed to download {image_url}")

    return downloaded_images
