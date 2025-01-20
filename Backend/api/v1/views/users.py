#!/usr/bin/env python3
""" API endpoints for the users """


from . import views_bp
from models.base import db
from models.user import User, user_roles
from models.plan import Plan
from models.role import Role
from models.custom_exercise import CustomExercise
from models.record import Record
from flask import request, jsonify, abort, url_for
from google_api import ManageDrive
import os
from flask_jwt_extended import jwt_required
from decorators import roles_required

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import joinedload


# Function to log SQL statements
def log_sql_statements(conn, cursor, statement, parameters, context, executemany):
    print(f"SQL Statement: {statement}")
    print(f"Parameters: {parameters}")

# Attach the logging function to the SQLAlchemy engine
event.listen(Engine, "before_cursor_execute", log_sql_statements)


drive = ManageDrive()


@views_bp.route('/users', methods=['GET'], strict_slashes=False)
@roles_required("Developer", "Admin")
def get_all_users():
    """ Retrieve all the users from the database """
    query = db.select(User)
    users = db.session.execute(query).scalars().all()

    if not users:
        return jsonify([]), 200
    # Return the users as a json object
    return jsonify([user.to_dict() for user in users]), 200


@views_bp.route('/users/<int:user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_one_user(user_id):
    """ Retrieve a single user from the database """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found"), 200
    # Return the user as a json object
    return jsonify(user.to_dict()), 200


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
        return abort(409, description="Conflict: Email already in use")
    
    # Create a new user
    print(type(data["password"]))
    new_user = User(**data)
    # new_user.password = data["password"]  # Hash the password

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return the user as a json object
    return jsonify(new_user.to_dict()), 201



@views_bp.route("/users/<int:user_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
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
            old_password = data.get("old_password")
            if not old_password:
                return abort(400, description="Bad Request: Missing old password")
            if not user.check_password(old_password):
                return abort(400, description="Bad Request: Incorrect old password")
            key = "password"
            value = data["new_password"]
        setattr(user, key, value)
    
    # Save the updated user back to the database
    db.session.commit()

    return jsonify(user.to_dict()), 200


@views_bp.route("/users/<int:user_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def remove_user(user_id):
    """Remove a user object"""

    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")

    # Delete the user's folder from drive
    user_folder = drive.find_folder_id("user_" + str(user_id), drive.users_folder_id)
    if user_folder:
        try:
            result, message = drive.delete_folder(folder_id=user_folder)
            if not result:
                return abort(500, description=f"Internal Server Error: {message}")
        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}")
        
    
    # Remove the user from the database
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


#--------------------------------- User Roles ---------------------------------#


# Endpoint to get all roles of a user
@views_bp.route('/users/<int:user_id>/roles', methods=['GET'], strict_slashes=False)
@roles_required("Developer", "Admin")
def get_user_roles(user_id):
    user = db.session.get(User, user_id)

    print(f"User found: {user}") # Debugging print
    if user is None:
        return abort(404, description="User not found")

    user_roles = [role.to_dict() for role in user.roles]
    return jsonify(user_roles), 200


# Endpoint to assign a role to a user
@views_bp.route('/users/<int:user_id>/roles/<role_name>', methods=['POST'], strict_slashes=False)
@roles_required("Admin")
def assign_role(user_id, role_name):
    # user = db.session.get(User, user_id)
    user = db.session.query(User).filter_by(id=user_id).first()


    if not user:
        return abort(404, description="User not found")
    
    # Check if the role already exists
    role = db.session.query(Role).filter_by(name=role_name).first()

    if not role:
        return abort(404, description="Role not found")

    db.session.refresh(user)  # Reload the user object

    # Check if the user already has the role
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        print(f"Role '{role_name}' assigned to user {user_id}") # Debug print
        print(f"User {user_id} roles after assignment: {[role.name for role in user.roles]}")
        return jsonify({"message": "Role assigned successfully"}), 201
    print(f"User {user_id} already has role '{role_name}'") # Debugging print
    return jsonify({"message": "User already has this role"}), 200

# Endpoint to assign a role to a user
# @views_bp.route('/users/<int:user_id>/roles/<role_name>', methods=['POST'], strict_slashes=False)
# @roles_required("Admin")
# def assign_role(user_id, role_name):
#     try:
#         print(f"Assigning role '{role_name}' to user with ID {user_id}")  # Debug print
#         user = db.session.get(User, user_id)
#         query = db.select(Role).where(Role.name == role_name)
#         role = db.session.execute(query).scalar()

#         if not user or not role:
#             print("User or Role not found")  # Debug print
#             return abort(404, description="User or Role not found")

#         print(f"User {user_id} roles before assignment: {[role.name for role in user.roles]}")  # Debug print

#         if role not in user.roles:
#             # Explicitly manage the session state to avoid conflicts
#             with db.session.begin_nested():
#                 user.roles.append(role)
#                 db.session.add(user)  # Ensure the user object is part of the session

#                 # Explicitly log session state before flush
#                 print("Session state before flush:", db.session.identity_map.items())

#                 db.session.flush()  # Flush changes to the database to track them

#                 # Explicitly log session state after flush
#                 print("Session state after flush:", db.session.identity_map.items())

#             print(f"User {user_id} roles after appending: {[role.name for role in user.roles]}")  # Debug print

#             db.session.commit()
#             print(f"Role '{role_name}' assigned to user {user_id}")  # Debug print
#             print(f"User {user_id} roles after assignment: {[role.name for role in user.roles]}")  # Debug print

#             return jsonify({"message": "Role assigned successfully"}), 201

#         print(f"User {user_id} already has role '{role_name}'")  # Debug print
#         return jsonify({"message": "User already has this role"}), 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error assigning role: {e}")  # Debug print
#         return jsonify({"message": "Error assigning role"}), 500

#     finally:
#         db.session.close()


# Endpoint to remove a role from a user
@views_bp.route('/users/<int:user_id>/roles/<role_name>', methods=['DELETE'], strict_slashes=False)
@roles_required("Admin")
def remove_role(user_id, role_name):
    """
    Remove a role from a user
    """
    user = db.session.get(User, user_id)
    if not user:
        return abort(404, description="User not found")
    
    role = Role.find_role_by_name(role_name)
    if not role:
        return abort(404, description="Role not found")
    
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return jsonify({"message": "Role removed successfully"}), 200
    
    return jsonify({"message": "User does not have this role"}), 200


# Endpoint to update a user's role
@views_bp.route('/users/<int:user_id>/roles/<role_name>', methods=['PUT'], strict_slashes=False)
def update_user_role(user_id, role_name):
    """
    Update a user's role
    """
    user = db.session.get(User, user_id)
    if not user:
        return abort(404, description="User not found")
    
    role = Role.find_role_by_name(role_name)
    if not role:
        return abort(404, description="Role not found")
    
    if role in user.roles:
        return jsonify({"message": "User already has this role"}), 200
    
    user.roles.append(role)
    db.session.commit()
    return jsonify({"message": "Role updated successfully"}), 200


# @views_bp.route('/users/<int:user_id>/roles/<role_name>', methods=['PUT'], strict_slashes=False)
# def update_user_role(user_id, role_name):
#     """
#     Update a user's role
#     """
#     try:
#         user = db.session.get(User, user_id)
#         if not user:
#             return abort(404, description="User not found")

#         role = Role.find_role_by_name(role_name)
#         if not role:
#             return abort(404, description="Role not found")

#         # Check if the user already has the role
#         user_roles_entry = db.session.execute(
#             db.select(user_roles).where(user_roles.c.user_id == user.id, user_roles.c.role_id == role.id)
#         ).fetchone()

#         if user_roles_entry:
#             return jsonify({"message": "User already has this role"}), 200

#         # Manually insert the new role to avoid triggering DELETE statements
#         db.session.execute(user_roles.insert().values(user_id=user.id, role_id=role.id))
#         db.session.commit()
#         return jsonify({"message": "Role updated successfully"}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": f"Error updating role: {e}"}), 500

#     finally:
#         db.session.close()



#--------------------------------- Profile Picture Upload, Update and Delete ---------------------------------#

@views_bp.route('/users/<int:user_id>/profile_picture', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_profile_picture(user_id):
    """ Retrieve the profile picture for the user """
    user = db.session.get(User, user_id)

    if user is None:
        return abort(404, description="User not found")
    
    # Check if the user has a profile picture
    if user.profile_picture is None:
        return abort(404, description="Profile picture not found")
    
    # Return the profile picture as a json object
    return jsonify({"file_url": user.profile_picture}), 200


@views_bp.route('/users/<int:user_id>/upload_profile_picture', methods=['POST'], strict_slashes=False)
@jwt_required()
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
@jwt_required()
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

    old_profile_picture_url = user.profile_picture

    # Save the new profile picture to a temporary location
    directory_path = f'tmp/fitjourney/user_{user_id}/profilepic'
    file_path = f"{directory_path}/{profile_picture.filename}"
    os.makedirs(directory_path, exist_ok=True)
    profile_picture.save(file_path)
    
    # Upload the new profile picture to Google Drive
    try:
        profile_pic_folder = drive.find_folder_id("profilepic", drive.find_folder_id("user_" + str(user_id), drive.users_folder_id))
        if not profile_pic_folder:
            return abort(404, description="Profile picture folder not found, please upload a new profile picture")
        file_id, web_view_link, web_content_link = drive.upload_file(file_path, profile_pic_folder)
        if not file_id:
            os.remove(file_path)
            return abort(500, description=f"Failed to upload new profile picture, The old profile_picture_url: {old_profile_picture_url}")

        # Update the user's profile picture URL in the database
        web_content_link = web_content_link.split("&")[0]
        user.profile_picture = web_content_link
        db.session.commit()
    except Exception as e:
        return abort(500, description=f"Internal Server Error: {e}, The Old profile_picture_url: {old_profile_picture_url}")

    # Delete the old profile picture if it exists
    print(old_profile_picture_url)
    if old_profile_picture_url:
        try:
            result, message = drive.delete_file(webContentLink=old_profile_picture_url)
            print(result, message)
            if not result:
                return abort(500, description=f"Failed to delete old profile picture: {message}, The New profile_picture_url: {web_content_link}")
        except Exception as e:
            return abort(500, description=f"Internal Server Error: {e}, The New profile_picture_url: {web_content_link}")

        # Remove the file from the temp folder
        os.remove(file_path)
        return jsonify({"message": "Profile picture updated successfully", "new_profile_picture_url": web_content_link}), 200


@views_bp.route('/users/<int:user_id>/delete_profile_picture', methods=['DELETE'], strict_slashes=False)
@jwt_required()
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
