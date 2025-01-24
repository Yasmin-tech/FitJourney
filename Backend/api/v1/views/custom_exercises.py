#!/usr/bin/env python3
""" API endpoints for the custom_exercise """


from . import views_bp
from models.base import db
from models.custom_exercise import CustomExercise
from models.user import User
from flask import request, jsonify, abort, url_for
from google_api import ManageDrive
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from decorators import roles_required, user_exists


drive = ManageDrive()


@views_bp.route('/custom_exercises', methods=['GET'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def get_all_custom_exercises():
    """ Retrieve all the custom exercises from the database """
    query = db.select(CustomExercise)
    custom_exercises = db.session.execute(query).scalars().all()

    if not custom_exercises:
        return jsonify([]), 200
    # Return the custom_exercises as a list json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in custom_exercises]), 200


@views_bp.route('/custom_exercises/title/<string:title>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_custom_exercise_by_title(title):
    """ Retrieve a single custom_exercise from the database """
    custom_exercise = db.session.query(CustomExercise).filter_by(title=title).first()

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if custom_exercise.user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Return the custom_exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route('/custom_exercises/categories', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_all_custom_exercise_categories():
    """ Retrieve all the custom exercise categories from the database """

    # get the use_id from the query parameters
    user_id = request.args.get('user_id', None)
    if user_id:
        user = db.session.get(User, user_id)
        if user is None:
            return abort(404, description="User not found")
        custom_exercises = user.custom_exercises
    else:
        abort(400, description="Bad Request: Missing user_id")
    
    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    if not custom_exercises:
            return jsonify([]), 200
    categories = db.session.query(CustomExercise.category).filter(CustomExercise.user_id == user_id).distinct().all()
    categories = [category[0] for category in categories]  # Extract the values from the tuples
    
    # Return the categories as a list json object
    return jsonify(categories), 200


@views_bp.route('/custom_exercises/muscle_groups', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_all_custom_exercise_muscle_groups():
    """ Retrieve all muscle groups of the exercises crested by the user from the database """

    # get the use_id from the query parameters
    user_id = request.args.get('user_id', None)
    if user_id:
        user = db.session.get(User, user_id)
        if user is None:
            return abort(404, description="User not found")
        custom_exercises = user.custom_exercises
    else:
        abort(400, description="Bad Request: Missing user_id")
    
    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    if not custom_exercises:
            return jsonify([]), 200
    muscle_groups = db.session.query(CustomExercise.muscle_group).filter(CustomExercise.user_id == user_id).distinct().all()
    muscle_groups = [muscle_group[0] for muscle_group in muscle_groups]
    return jsonify(muscle_groups), 200


@views_bp.route('/custom_exercises/muscle_groups/<string:muscle_group>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_all_custom_exercises_by_muscle_group(muscle_group):
    """ Retrieve all the custom exercises by muscle group from the database """

    # get the use_id from the query parameters
    user_id = request.args.get('user_id', None)
    if user_id:
        user = db.session.get(User, user_id)
        if user is None:
            return abort(404, description="User not found")
        custom_exercises = user.custom_exercises
    else:
        abort(400, description="Bad Request: Missing user_id")
    
    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    if not custom_exercises:
            return jsonify([]), 200
    custom_exercises = db.session.query(CustomExercise).filter(CustomExercise.user_id == user_id, CustomExercise.muscle_group == muscle_group).all()

    return jsonify([custom_exercise.to_dict() for custom_exercise in custom_exercises]), 200


@views_bp.route('/custom_exercises/<int:custom_exercise_id>', methods=['GET'], strict_slashes=False)
@roles_required('Admin', 'Developer')
def get_one_custom_exercise(custom_exercise_id):
    """ Retrieve a single custom_exercise from the database """
    custom_exercise = db.session.get(CustomExercise, custom_exercise_id)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    # Return the exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route('/users/<int:user_id>/custom_exercises', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_user_custom_exercises(user_id):
    """ Retrieve all the custom exercises from a specific user """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Return the custom_exercises as a list json object
    return jsonify([custom_exercise.to_dict() for custom_exercise in user.custom_exercises]), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_user_custom_exercise(user_id, custom_exercise_id):
    """ Retrieve a single custom_exercise from a specific user """

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    # Return the custom_exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200

@views_bp.route('/users/<int:user_id>/custom_exercises', methods=['POST'], strict_slashes=False)
@jwt_required()
@user_exists
def create_exercise_fot_user(user_id):
    """ Create a new exercise for a specific user """
    
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

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
    query = db.select(CustomExercise).where(CustomExercise.title == data["title"], CustomExercise.user_id == user_id)
    custom_exercise = db.session.execute(query).scalar()

    if custom_exercise:
        return abort(409, description="Conflict: Custom Exercise already exists")
    
    # Create the new exercise
    new_custom_exercise = CustomExercise(**data, user_id=user_id)
    db.session.add(new_custom_exercise)
    db.session.commit()
    # Return the new exercise as a json object
    return jsonify(new_custom_exercise.to_dict()), 201


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
@user_exists
def update_custom_exercise(user_id, custom_exercise_id):
    """ Update an existing exercise """
    
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["title", "description", "category", "muscle_group", "equipment", "media_file_url"]
    
    # Update the exercise
    for key, value in data.items():
        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid Key {key}")
        setattr(custom_exercise, key, value)
    db.session.commit()
    # Return the updated exercise as a json object
    return jsonify(custom_exercise.to_dict()), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@user_exists
def delete_custom_exercise(user_id, custom_exercise_id):
    """ Delete the custom_exercise from the database """
    
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    
    # Delete this exercise file in Google Drive
    if custom_exercise.media_file_url:
        try:
            result, message = drive.delete_file(webContentLink=custom_exercise.media_file_url)
            print(result, message)
            if not result:
                # if google drive return false, the file is not in drive
                custom_exercise.media_file_url = None
        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")

    db.session.delete(custom_exercise)
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Custom Exercise deleted successfully"}), 200


# -----Manage uploading, updating and deleting exercises images and videos in google drive----------------------

@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>/media_file', methods=['GET'], strict_slashes=False)
@jwt_required()
@user_exists
def get_custom_exercise_media_file(user_id, custom_exercise_id):
    """ Retrieve the media file stored as a url for the exercise """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    #Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    # Check if the exercise has a media file
    if custom_exercise.media_file_url is None:
        return abort(404, description="Media file not found")
    
    # Return the media file url as a json object
    return jsonify({"media_file_url": custom_exercise.media_file_url}), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>/upload_media', methods=['POST'], strict_slashes=False)
@jwt_required()
@user_exists
def upload_media(user_id, custom_exercise_id):
    """ Upload the media for the custom_exercise to Google Drive """
    
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    
    # access the query parameters
    media_file_url = request.args.get('media_file_url', None)

    # if url is provided, save it directly to the database
    if media_file_url:
        custom_exercise.media_file_url = media_file_url
        db.session.commit()
        return jsonify({"message": f"The exercise media has been created successfully {media_file_url}"}), 201

    # Upload the media to Google Drive if payload exists
    media_file = request.files.get('media_file', None)
    if not media_file:
        return abort(400, description="Bad Request: Missing media file")

    if media_file.filename == "":
        return abort(400, description="Bad Request: Media file is not selected")


    # save path to the media file locally

    directory_path = f'tmp/fitjourney/user_{user_id}/exercises'
    media_file_name = f'file_{custom_exercise_id}_' + media_file.filename
    print(media_file_name)
    file_path = f"{directory_path}/{media_file_name}"
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    # Save the file to the temp folder
    media_file.save(file_path)

    # Upload the file to Google Drive
    root_folder = drive.root_folder_id
    users = drive.users_folder_id
 
    # Create a folder for the current user if it doesn't exist
    user_folder = drive.find_folder_id(f"user_{user_id}", users)
    if not user_folder:
        user_folder = drive.create_folder(f"user_{user_id}", users)

    # Create folder for exercises if it doesn't exist
    exercises_folder = drive.find_folder_id("exercises", user_folder)
    if not exercises_folder:
        exercises_folder = drive.create_folder("exercises", user_folder)

    file_id, file_url = drive.find_file_id(media_file_name, exercises_folder)
    if file_id:
        os.remove(file_path)
        return abort(400, description=f"Bad Request: File already exists {file_url.split('&')[0]}")


    file_id, supported_file_type, web_content_link = drive.upload_file(file_path, exercises_folder)
    os.remove(file_path)

    if not supported_file_type:
        return abort(400, description="Bad Request: Unsupported file type")

    if web_content_link:
        web_content_link = web_content_link.split("&")[0]
    else:
        return abort(500, description="Internal Server Error: An error occurred while uploading the file")

    # Update the media_file_url in the database
    custom_exercise.media_file_url = web_content_link
    db.session.commit()
    # Return the custom_exercise as a json object
    return jsonify({"message": f"The exercise media has been created successfully {web_content_link}"}), 201


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>/update_media', methods=['PUT'], strict_slashes=False)
@jwt_required()
@user_exists
def update_media(user_id, custom_exercise_id):
    """ Update the media for the custom_exercise """
    # Check if the user exists
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")

    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")
    
    # access the query parameters
    media_file_url = request.args.get('media_file_url', None)

    # if url is provided, save them directly to the database
    if media_file_url:
         # Delete the old media file
        old_media_file_url = custom_exercise.media_file_url
        if old_media_file_url:
            try:
                result, message = drive.delete_file(webContentLink=old_media_file_url)
                print(result, message)
                if not result:
                    # if google drive return false, the file is not in drive
                    custom_exercise.media_file_url = None

            except Exception as e:
                return abort(500, description=f"Internal Server Error: {e}")
        custom_exercise.media_file_url = media_file_url
        db.session.commit()
        return jsonify({"message": f"The exercise media has been updated successfully {media_file_url}"}), 200

    # Check payload for media file
    media_file = request.files.get('media_file', None)
    if not media_file:
        return abort(400, description="Bad Request: Missing media file")

    if media_file.filename == "":
        return abort(400, description="Bad Request: Media file is not selected")

    # save path to the media file locally

    directory_path = f'tmp/fitjourney/user_{user_id}/exercises'
    media_file_name = f'file_{custom_exercise_id}_' + media_file.filename
    print(media_file_name)
    file_path = f"{directory_path}/{media_file_name}"
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    # Save the file to the temp folder
    media_file.save(file_path)

    # Create folder for exercises if it doesn't exist
    user_folder = drive.find_folder_id(f"user_{user_id}", drive.users_folder_id)
    if not user_folder:
        user_folder = drive.create_folder(f"user_{user_id}", drive.users_folder_id)
    exercises_folder = drive.find_folder_id("exercises", user_folder)
    if not exercises_folder:
        exercises_folder = drive.create_folder("exercises", user_folder)

    file_id, file_url = drive.find_file_id(media_file_name, exercises_folder)
    if file_id:
        os.remove(file_path)
        return abort(400, description=f"Bad Request: File already exists {file_url.split('&')[0]}")


    file_id, supported_file_type, web_content_link = drive.upload_file(file_path, exercises_folder)
    os.remove(file_path)

    if not supported_file_type:
        return abort(400, description="Bad Request: Unsupported file type")

    if web_content_link:
        web_content_link = web_content_link.split("&")[0]
    else:
        return abort(500, description="Internal Server Error: An error occurred while uploading the file")
    
     # Delete the old media file
    old_media_file_url = custom_exercise.media_file_url
    if old_media_file_url:
        try:
            result, message = drive.delete_file(webContentLink=old_media_file_url)
            print(result, message)
            # if google drive return false, the file is not in drive
            custom_exercise.media_file_url = None

        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")

    # Update the media_file_url in the database
    custom_exercise.media_file_url = web_content_link
    db.session.commit()
    return jsonify({"message": f"The exercise media has been updated successfully {web_content_link}"}), 200


@views_bp.route('/users/<int:user_id>/custom_exercises/<int:custom_exercise_id>/delete_media', methods=['DELETE'], strict_slashes=False)
@jwt_required()
@user_exists
def delete_media(user_id, custom_exercise_id):
    """ Delete the media file for the exercise """

    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check the log in user credentials
    log_in_user_email = get_jwt_identity()
    log_in_user = db.session.query(User).filter_by(email=log_in_user_email).first()
    roles = [role.name for role in log_in_user.roles]
    # print(plan.user.email)
    # print(log_in_user_email)
    if user.email != log_in_user_email and 'Admin' not in roles and 'Developer' not in roles:
        return abort(403, description="Forbidden: User does not have access to this resource")

    # Check if the custom_exercise exists
    custom_exercise = next((custom_exercise for custom_exercise in user.custom_exercises if custom_exercise.id == custom_exercise_id), None)

    if custom_exercise is None:
        return abort(404, description="Custom Exercise not found")

    # Check if the exercise has a media file
    if custom_exercise.media_file_url is None:
        return abort(404, description="Media file not found")

    media_file_url = custom_exercise.media_file_url
    try:
        result, message = drive.delete_file(webContentLink=media_file_url)
        print(result, message)
        if result is True:
            custom_exercise.media_file_url = None
            db.session.commit()
            return jsonify({"message": message}), 200
        
        # if google drive return false, the file is not in drive
        custom_exercise.media_file_url = None
        db.session.commit()
        return jsonify({"message": "media file deleted successfully"}), 200
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}")
