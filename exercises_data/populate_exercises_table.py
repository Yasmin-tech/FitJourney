#!/usr/bin/env python3 
"""
    Description: This script reads the newExercisesDataset.csv file
    and sends POST requests to the API to populate the exercises table.
    """


import pandas as pd
import requests


# Read the CSV file
df = pd.read_csv('newExercisesDataset.csv')

# Handle NaN values
df.fillna('', inplace=True)

# Endpoint URL
url = 'http://localhost:5001/api/v1/exercises'

# Send a GET request to the endpoint
# response = requests.get(url)
# print(response.json())
# print(response.text)


# Iterate over each row in the DataFrame
def send_post_request():
    """ Send POST requests to the API to populate the exercises table """
    for index, row in df.iterrows():
        # Create the payload
        payload = {
            'title': row['title'],
            'description': row['description'],
            'category': row['category'],
            'muscle_group': row['muscleGroup'],
            'equipment': row['equipment']
        }
        # if the status code is not 201 or not 409, print the response and break the loop
        response = requests.post(url, json=payload)
        if response.status_code != 201 and response.status_code != 409:
            print(f"Error: {response.text}")
            break
        # Send the POST request
        
        # Print the response for debugging
        print(f"Response for row {index}: {response.status_code} - {response.text}")

    print("All POST requests sent!")

# Call the function to send POST requests
# send_post_request()
