#!/usr/bin/env python3
import pandas as pd

# Load the existing CSV file
df = pd.read_csv("megaGymDataset.csv")

# # Define the mapping of old body parts to unified categories
# body_part_mapping = {
#     'Abdominals': 'Abdominals',
#     'Adductors': 'Adductors',
#     'Abductors': 'Abductors',
#     'Biceps': 'Biceps',
#     'Calves': 'Calves',
#     'Chest': 'Chest',
#     'Forearms': 'Forearms',
#     'Glutes': 'Glutes',
#     'Hamstrings': 'Hamstrings',
#     'Lats': 'Back',
#     'Lower Back': 'Back',
#     'Middle Back': 'Back',
#     'Traps': 'Traps',
#     'Neck': 'Neck',
#     'Quadriceps': 'Quadriceps',
#     'Shoulders': 'Shoulders',
#     'Triceps': 'Triceps'
# }

# # Map the 'BodyPart' column to unified categories
# df['muscleGroup'] = df['BodyPart'].map(body_part_mapping)

# # Select specific columns and rename them
# df_new = df[['Title', 'Desc', 'Type', 'Equipment', 'muscleGroup']]
# df_new.columns = ['title', 'description', 'category','equipment', 'muscleGroup']

# # Save the new DataFrame to a new CSV file
# df_new.to_csv('newExercisesDataset.csv', index=False)

# print("New CSV file created successfully!")

df_new = pd.read_csv("newExercisesDataset.csv")
print(df_new.isnull().sum())
print(df_new.duplicated().sum())
