#!/usr/bin/env python3
""" API endpoints for the users """


from . import views_bp
from models.base import db
from models.user import User
from models.plan import Plan
from models.custom_exercise import CustomExercise
from models.record import Record
from flask import request, jsonify, abort, url_for
from google_api import ManageDrive
import os


drive = ManageDrive()


@views_bp.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieve all the users from the database """
    query = db.select(User)
    users = db.session.execute(query).scalars().all()

    if not users:
        return jsonify([]), 200
    # Return the users as a json object
    return jsonify([user.to_dict() for user in users])


@views_bp.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_one_user(user_id):
    """ Retrieve a single user from the database """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    # Return the user as a json object
    return jsonify(user.to_dict())


@views_bp.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new user """
   
    data = request.get_json()
    # Check if the request is a json object
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    # Check if the required fields are in the json object
    if "first_name" not in data:
        return abort(400, description="Bad Request: Missing first_name")
    if "last_name" not in data:
        return abort(400, description="Bad Request: Missing last_name")
    if "email" not in data:
        return abort(400, description="Bad Request: Missing email")
    if "password" not in data:
        return abort(400, description="Bad Request: Missing password")
    
    # Check if the email is already in use
    query = db.select(User).where(User.email == data["email"])
    user = db.session.execute(query).scalar()

    if user:
        return abort(400, description="Bad Request: Email already in use")
    
    # Create a new user
    new_user = User(**data)
    # new_user.password = data["password"]  # Hash the password

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return the user as a json object
    return jsonify(new_user.to_dict()), 201



@views_bp.route("/users/<int:user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a user object"""

    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check if the request is a json object
    data = request.get_json()
    if not data:
        return abort(400, description="Bad Request: Not a JSON")
    
    allowed_keys = ["first_name", "last_name", "old_password", "new_password"]
    # Update the user object
    for key, value in data.items():

        if key not in allowed_keys:
            return abort(400, description=f"Bad Request: Invalid key {key}")
        # Verify old password when changing password
        if key == "new_password":
            if not user.check_password(data["old_password"]):
                return abort(400, description="Bad Request: Incorrect old password")
            key = "password"
            value = data["new_password"]
        setattr(user, key, value)
    
    # Save the updated user back to the database
    db.session.commit()

    return jsonify(user.to_dict()), 200


@views_bp.route("/users/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def remove_user(user_id):
    """Remove a user object"""

    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")

    # Delete the user's folder from drive
    user_folder = drive.find_folder_id("user_" + str(user_id), drive.users_folder_id)
    if user_folder:
        try:
            result, message = drive.delete_file(file_id=user_folder)
            if not result:
                return abort(500, description=f"Internal Server Error: {message}")
        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")
        
    
    # Remove the user from the database
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


@views_bp.route('/users/<int:user_id>/profile_picture', methods=['GET'], strict_slashes=False)
def get_profile_picture(user_id):
    """ Retrieve the profile picture for the user """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check if the user has a profile picture
    if user.profile_picture is None:
        return abort(404, description="Profile picture not found")
    
    # Return the profile picture as a json object
    return jsonify({"file_url": user.profile_picture})


@views_bp.route('/users/<int:user_id>/upload_profile_picture', methods=['POST'], strict_slashes=False)
def upload_profile_picture(user_id):
    """ Upload a profile picture for the user """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check if the request has a file
    if "file" not in request.files:
        return abort(400, description="Bad Request: No file part")
    
    profile_picture = request.files.get("file")
    if profile_picture.filename == "":
        return abort(400, description="Bad Request: No selected file")
    
    # Create user directory and subdirectory for profile pictures in Drive
    # try:

    # Get the root folder
    root_folder = drive.root_folder_id
    users = drive.users_folder_id

    current_user_folder_name = f"user_{user_id}"
    # Create a folder for the current user if it doesn't exist
    user_folder = drive.find_folder_id(current_user_folder_name, users)
    if not user_folder:
        user_folder = drive.create_folder(current_user_folder_name, users)
    
    # print(user_folder)

    # Create a folder for the profile pictures if it doesn't exist
    profile_pic_folder = drive.find_folder_id("profilepic", user_folder)
    if not profile_pic_folder:
        profile_pic_folder = drive.create_folder("profilepic", user_folder)

    # print(profile_pic_folder)

    # Construct the file path
    directory_path = f'tmp/fitjourney/user_{user_id}/profilepic'
    file_path = f"{directory_path}/{profile_picture.filename}"
    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)

    # Save the file to the temp folder
    profile_picture.save(file_path)

    file_id, file_url = drive.find_file_id(profile_picture.filename, profile_pic_folder)
    if file_id:
        return abort(400, description=f"Bad Request: File already exists {file_url.split('&')[0]}")

    # Upload the file to drive
    file_id, web_view_link, web_content_link = drive.upload_file(file_path, profile_pic_folder)

    web_content_link = web_content_link.split("&")[0]

    # print(f"File ID: {file_id}")
    # print(f"Web View Link: {web_view_link}")
    # print(f"Web Content Link: {web_content_link}")

    # Update the user profile picture URL in the database
    user.profile_picture = web_content_link
    db.session.commit()
    # Remove the file from the temp folder
    os.remove(file_path)

    # Return the file url as a json object
    return jsonify({"message": "File uploaded successfully" ,"file_url": web_content_link}), 201


@views_bp.route('/users/<int:user_id>/update_profile_picture', methods=['PUT'], strict_slashes=False)
def update_profile_picture(user_id):
    """ Update the profile picture for the user """
    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")
    
    if "file" not in request.files:
        return abort(400, description="Bad Request: No file part")
    
    profile_picture = request.files.get("file")
    if profile_picture.filename == "":
        return abort(400, description="Bad Request: No selected file")

    # Delete the old profile picture if it exists
    old_profile_picture_url = user.profile_picture
    print(old_profile_picture_url)
    if old_profile_picture_url:
        try:
            result, message = drive.delete_file(webContentLink=old_profile_picture_url)
            print(result, message)
            if not result:
                return abort(500, description=f"Failed to delete old profile picture: {message}")
        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")

    # Save the new profile picture to a temporary location
    directory_path = f'tmp/fitjourney/user_{user_id}/profilepic'
    file_path = f"{directory_path}/{profile_picture.filename}"
    os.makedirs(directory_path, exist_ok=True)
    profile_picture.save(file_path)
    
    # Upload the new profile picture to Google Drive
    try:
        profile_pic_folder = drive.find_folder_id("profilepic", drive.find_folder_id("user_" + str(user_id), drive.users_folder_id))
        file_id, web_view_link, web_content_link = drive.upload_file(file_path, profile_pic_folder)
        if not file_id:
            return abort(500, description="Failed to upload new profile picture")

        # Update the user's profile picture URL in the database
        web_content_link = web_content_link.split("&")[0]
        user.profile_picture = web_content_link
        db.session.commit()

        # Remove the file from the temp folder
        os.remove(file_path)
        return jsonify({"message": "Profile picture updated successfully", "new_profile_picture_url": web_content_link}), 200
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}")


@views_bp.route('/users/<int:user_id>/delete_profile_picture', methods=['DELETE'], strict_slashes=False)
def delete_profile_picture(user_id):
    """ Delete the profile picture for the user """

    user = db.session.get(User, user_id)
    if user is None:
        return abort(404, description="User not found")
    
    profile_picture_url = user.profile_picture
    if not profile_picture_url:
        return abort(404, description="Profile picture not found")

    try:
        result, message = drive.delete_file(webContentLink=profile_picture_url)
        
        if result is True:
            # update the user profile picture to None
            user.profile_picture = None
            db.session.commit()
            return jsonify({"message": message}), 200
        
        return abort(500, description=f"Internal Server Error: {message}")
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}")
