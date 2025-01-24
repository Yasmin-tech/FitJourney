#!/usr/bin/env python3
""" API endpoints for the exercises """


from . import views_bp
from models.base import db
from models.exercise import Exercise
from flask import request, jsonify, abort, url_for
import os
from google_api import ManageDrive
from decorators import roles_required, user_exists
from flask_jwt_extended import jwt_required


drive = ManageDrive()


# @views_bp.route('/exercises', methods=['GET'], strict_slashes=False)
# @roles_required('Admin', 'Developer')
# def get_all_exercises():
#     """ Retrieve all the exercises from the database """
#     query = db.select(Exercise)
#     exercises = db.session.execute(query).scalars().all()

#     if not exercises:
#         return jsonify([]), 200
#     # Return the exercises as a json object
#     return jsonify([exercise.to_dict() for exercise in exercises]), 200

@views_bp.route('/exercises', methods=['GET'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def get_all_exercises():
    """ Retrieve all the exercises from the database with pagination """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = db.select(Exercise).offset((page - 1) * per_page).limit(per_page)
    exercises = db.session.execute(query).scalars().all()
    
    total_exercises = db.session.query(Exercise).count()
    total_pages = (total_exercises + per_page - 1) // per_page

    if not exercises:
        return jsonify([]), 200

    response = {
        'exercises': [exercise.to_dict() for exercise in exercises],
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_exercises': total_exercises
    }

    return jsonify(response), 200


@views_bp.route('/exercises/<int:exercise_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_one_exercise(exercise_id):
    """ Retrieve a single exercise from the database """
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    # Return the exercise as a json object
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/exercises/title/<string:title>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_exercise_by_title(title):
    """ Retrieve an exercise by its title """
    exercise = db.session.query(Exercise).filter_by(title=title).first()
    if not exercise:
        return abort(404, description="Exercise not found")
    
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/exercises/categories', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_all_categories():
    """ Retrieve all unique exercise categories """
    categories = db.session.query(Exercise.category).distinct().all()
    categories = [category[0] for category in categories]  # Extract the values from the tuples
    return jsonify(categories), 200


@views_bp.route('/exercises/muscle_groups', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_all_muscle_groups():
    """ Retrieve a list of all unique muscle groups that exercises target """
    muscle_groups = db.session.query(Exercise.muscle_group).distinct().all()
    muscle_groups = [item[0] for item in muscle_groups]  # Extract the values from the tuples
    return jsonify(muscle_groups), 200


@views_bp.route('/exercises/muscle_groups/<string:muscle_group>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_exercises_by_muscle_group(muscle_group):
    """ Retrieve exercises that target a specific body part """
    exercises = db.session.query(Exercise).filter_by(muscle_group=muscle_group).all()
    if not exercises:
        return jsonify([]), 200
    
    return jsonify([exercise.to_dict() for exercise in exercises]), 200


@views_bp.route('/exercises', methods=['POST'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def create_exercise():
    """ Create a new exercise """
    
    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "title" not in data:
        return abort(400, description="Bad Request: Missing title")
    if "category" not in data:
        return abort(400, description="Bad Request: Missing category")
    if "muscle_group" not in data:
        return abort(400, description="Bad Request: Missing muscle_group")
    
    # Check if the exercise already exists
    query = db.select(Exercise).where(Exercise.title == data["title"])
    exercise = db.session.execute(query).scalar()

    if exercise:
        return abort(409, description="Conflict: Exercise already exists")
    
    # Create the new exercise
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    # Return the new exercise as a json object
    return jsonify(exercise.to_dict()), 201


@views_bp.route('/exercises/<int:exercise_id>', methods=['PUT'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def update_exercise(exercise_id):
    """ Update an existing exercise """
    
    # Check if the exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["title", "description", "category", "muscle_group", "equipment", "media_file_url"]
    
    # Update the exercise
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid Key {key}")
        setattr(exercise, key, value)
    db.session.commit()
    # Return the updated exercise as a json object
    return jsonify(exercise.to_dict()), 200


@views_bp.route('/exercises/<int:exercise_id>', methods=['DELETE'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def delete_exercise(exercise_id):
    """ Delete an exercise from the database """
    
    # Check if the exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    
    db.session.delete(exercise)
    db.session.commit()
    # Return a success message
    return jsonify({"message": "Exercise deleted successfully"}), 200


# -----Manage uploading, updating and deleting exercises images and videos in google drive----------------------

@views_bp.route('/exercises/<int:exercise_id>/media_file', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_exercise_media_file(exercise_id):
    """ Retrieve the media file stored as url for the exercise """
    
    # Check if the exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")

    # Check if the exercise has a media file
    if exercise.media_file_url is None:
        return abort(404, description="Media file not found")
    
    # Return the media file url as a json object
    return jsonify({"media_file_url": exercise.media_file_url}), 200


@views_bp.route('/exercises/<int:exercise_id>/upload_media', methods=['POST'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def upload_exercise_media(exercise_id):
    """ Upload the media for the exercise to Google Drive """

    # Check if the custom_exercise exists
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    
    # access the query parameters
    media_file_url = request.args.get('media_file_url', None)

    # if url is provided, save it directly to the database
    if media_file_url:
        exercise.media_file_url = media_file_url
        db.session.commit()
        return jsonify({"message": f"The exercise media has been created successfully {media_file_url}"}), 201

    # Upload the media to Google Drive if payload exists
    media_file = request.files.get('media_file', None)
    if not media_file:
        return abort(400, description="Bad Request: Missing media file")

    if media_file.filename == "":
        return abort(400, description="Bad Request: Media file is not selected")


    # save path to the media file locally

    directory_path = f'tmp/fitjourney/exercises'
    media_file_name = f'file_{exercise_id}_' + media_file.filename
    print(media_file_name)
    file_path = f"{directory_path}/{media_file_name}"
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    # Save the file to the temp folder
    media_file.save(file_path)

    # Upload the file to Google Drive
    default_exercises_folder = drive.default_exercises_folder

    file_id, file_url = drive.find_file_id(media_file_name, default_exercises_folder)
    if file_id:
        os.remove(file_path)
        return abort(400, description=f"Bad Request: File already exists {file_url.split('&')[0]}")

    file_id, supported_file_type, web_content_link = drive.upload_file(file_path, default_exercises_folder)
    os.remove(file_path)

    if not supported_file_type:
        os.remove(file_path)
        return abort(400, description="Bad Request: Unsupported file type")

    if web_content_link:
        web_content_link = web_content_link.split("&")[0]
    else:
        return abort(500, description="Internal Server Error: An error occurred while uploading the file")

    # Update the media_file_url in the database
    exercise.media_file_url = web_content_link
    db.session.commit()
    # Return the custom_exercise as a json object
    return jsonify({"message": f"The exercise media has been created successfully {web_content_link}"}), 201


@views_bp.route('/exercises/<int:exercise_id>/update_media', methods=['PUT'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def update_exercise__media(exercise_id):
    """ Update the media for the exercises """
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")
    
    # access the query parameters
    media_file_url = request.args.get('media_file_url', None)

    # if url is provided, save it directly to the database
    if media_file_url:
         # Delete the old media file
        old_media_file_url = exercise.media_file_url
        if old_media_file_url:
            try:
                result, message = drive.delete_file(webContentLink=old_media_file_url)
                print(result, message)
                if not result:
                    # if google drive return false, the file is not in drive
                    exercise.media_file_url = None

            except Exception as e:
                return abort(500, description=f"Internal Server Error: {e}")
        exercise.media_file_url = media_file_url
        db.session.commit()
        return jsonify({"message": f"The exercise media has been updated successfully {media_file_url}"}), 200


    # Check payload for media file
    media_file = request.files.get('media_file', None)
    if not media_file:
        return abort(400, description="Bad Request: Missing media file")

    if media_file.filename == "":
        return abort(400, description="Bad Request: Media file is not selected")

    # save path to the media file locally

    directory_path = f'tmp/fitjourney/exercises'
    media_file_name = f'file_{exercise_id}_' + media_file.filename
    print(media_file_name)
    file_path = f"{directory_path}/{media_file_name}"
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    # Save the file to the temp folder
    media_file.save(file_path)

    # Upload the file to Google Drive
    default_exercises_folder = drive.default_exercises_folder

    file_id, file_url = drive.find_file_id(media_file_name, default_exercises_folder)
    if file_id:
        os.remove(file_path)
        return abort(400, description=f"Bad Request: File already exists {file_url.split('&')[0]}")

    file_id, supported_file_type, web_content_link = drive.upload_file(file_path, default_exercises_folder)
    os.remove(file_path)

    if not supported_file_type:
        return abort(400, description="Bad Request: Unsupported file type")

    if web_content_link:
        web_content_link = web_content_link.split("&")[0]
    else:
        return abort(500, description="Internal Server Error: An error occurred while uploading the file")
    
    # Delete the old media file
    old_media_file_url = exercise.media_file_url
    if old_media_file_url:
        try:
            result, message = drive.delete_file(webContentLink=old_media_file_url)
            print(result, message)
            # if google drive return false, the file is not in drive
            exercise.media_file_url = None

        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")
    
    # Update the media_file_url in the database
    exercise.media_file_url = web_content_link
    db.session.commit()
    return jsonify({"message": f"The exercise media has been updated successfully {web_content_link}"}), 200


@views_bp.route('/exercises/<int:exercise_id>/delete_media', methods=['DELETE'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def delete_exercise_media(exercise_id):
    """ Delete the media file for the exercise """

    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return abort(404, description="Exercise not found")

    # Check if the exercise has a media file
    if exercise.media_file_url is None:
        return abort(404, description="Media file not found")

    media_file_url = exercise.media_file_url
    try:
        result, message = drive.delete_file(webContentLink=media_file_url)
        print(result, message)
        if result is True:
            exercise.media_file_url = None
            db.session.commit()
            return jsonify({"message": message}), 200
        
        # if google drive return false, the file is not in drive
        exercise.media_file_url = None
        db.session.commit()
        return jsonify({"message": "media file deleted successfully"}), 200
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}")
