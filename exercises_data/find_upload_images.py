#!/usr/bin/env python3
"""
    This script use web scraping to get the image URL for a given exercise name
    and then upload the image to each exercise in the database by sending
    a POST request to the API.
    """

import requests
from bs4 import BeautifulSoup


# Function to get the image URL for a given exercise name
import requests
import random

def get_unsplash_image(exercise_name, body_part, equipment):
    access_key = "_Ai-9KjerN2NE7aftuEdrSo8Ano6CR46Zevrn0DypEM"
    query = f"{exercise_name} {body_part} {equipment} exercise tutorial"
    url = f"https://api.unsplash.com/search/photos?page=1&query={query.replace(' ', '+')}&client_id={access_key}"
    response = requests.get(url)
    data = response.json()
    
    if not data['results']:
        return None  # Return None if no images are found

    # Randomly select an image from the search results
    image_url = random.choice(data['results'])['urls']['regular']
    # image_url = data['results'][0]['urls']['regular']
    return image_url

# Example usage
exercise_name = "Partner plank band row"
body_part = "triceps"
equipment = "machine"
image_url = get_unsplash_image(exercise_name, body_part, equipment)
print(image_url)

