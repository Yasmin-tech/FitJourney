## 💡FitJourney APP API  🧩 *Back-end Project*


<div align="center">
   <img src="https://i.imgur.com/hR6m5Nd.jpeg" alt="FitJourney Logo" />
    <h1>✨FitJorney API</h1>
</div>

## Table of Contents

- [Description](#description)
- [Purpose](#purpose)
- [Goals](#goals)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Setting Up the Database](#setting-up-the-database)
- [Running Swagger Documentation](#running-swagger-documentation)
- [Restarting the Server](#restarting-the-server)
- [Populating Exercises Table with Predefined Exercises](#populating-exercises-table-with-predefined-exercises)
- [A diagram that shows the user journey](#example-of-the-end-user-journey-in-the-app)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Description

FitJourney is a powerful fitness-tracking API designed to help users manage their workouts, monitor their progress, and efficiently achieve their fitness goals. Offering a comprehensive set of features for individuals of all fitness levels, from beginners to advanced athletes. 
The application relies on the **FitJourney APP API** to facilitate seamless interaction between the frontend and backend components. Users can easily manage their workout plans, detailing each day with predefined exercises targeting specific muscle groups. They also have the option to create their own exercises, complete with images or videos for proper execution. Additionally, users can log their daily exercise sessions, allowing them to track their progress and stay on course to achieve their fitness objectives.


## Purpose
The primary goal of the FitJourney APP API is to offer developers a powerful and versatile set of tools for creating their own fitness planning and tracking applications. By utilizing this API, developers can design apps that empower users to plan workout sessions, track exercises, monitor their progress, and access tailored fitness plans. The API is engineered for reliability and efficiency, ensuring smooth integration and interaction with various front-end applications.


## Goals

-   **User Management**: Enable users to create accounts, log in, upload a profile picture for personalization, and manage their profiles securely.

-   **Personalized Workout Plans**: Assist users in managing their workout plans by helping them define their goals, current weight, target weight, the duration of the plan in weeks, and the number of days they plan to exercise each week. Then, create a detailed daily plan that includes exercises. Users can either select predefined exercises from the system based on the target muscle groups or create their own custom exercises.

-   **Custom Exercises**: Users should be able to create their own exercise sets, including a description of each exercise and its instructions. They can categorize the exercises (e.g., Cardio, Strength), specify the muscle groups targeted, list any necessary equipment, and include images or videos to aid in performing the exercises correctly.

-   **Progress Monitoring**: Allow users to log their daily exercise sessions to help them track progress and achieve their fitness goals. Users can enter all relevant details of each exercise, including the number of sets and reps completed, the duration of rest between sets, the weight lifted in kilograms for strength training exercises, as well as the location and difficulty of the workout. This information will assist them in receiving feedback for their next session. Additionally, a notes section will be provided for users to record any observations or thoughts efficiently.

-   **Exercise Tracking**: Creating daily logs will enable users to see and track their progress and adjust their plans accordingly.


## Features

- ✔️  **Secure Authentication**: User authentication and authorization are implemented using JSON Web Tokens (JWT) to ensure a secure process.


- ✔️  **Password Security**: User passwords are not stored as plain text. Instead, they are hashed using bcrypt, a strong and secure hashing algorithm, to ensure that user credentials are protected.


- ✔️  **RESTful Endpoints**: A comprehensive set of RESTful endpoints allows for the execution of CRUD (Create, Read, Update, Delete) operations on users, workouts, exercises, and other entities.


- ✔️  **Data Validation**: Robust mechanisms for data validation are in place to ensure data integrity and consistency.


- ✔️  **Role-Based Access Control**: The system includes a main admin user who has access to all API endpoints and is responsible for granting access to other developers. Admins can create developer roles and assign them to engineers involved in the project. Certain endpoints are restricted to users with Admin or Developer roles.

- ✔️  **Predefined Exercises**: The API comes with over 2,000 predefined exercises, which can only be accessed by admins or developers. The dataset used to populate the exercises table is found in the `exercises_data` directory as `megaGymDataset.csv`. This data has been cleaned and processed using the `/exercises_data/data.py` script, resulting in the final `newExercisesDataset.csv`. To populate your local database, run the `populate_exercises_table.py` script, ensuring you pass the admin JWT tokens after uncommenting the last line. Note that there are no media files for the exercises, but you can send a POST request to add images or videos.

- ✔️  **Google Drive Integration**: The API utilizes Google Drive as a file storage solution for media files.

- ✔️  **Error Handling**: The system provides clear and informative error messages to help users and developers quickly understand and resolve any issues.

## Tech Stack

 🛠️ The FitJourney APP API is built using the following technologies:

- **Programming Language**:
  - 🐍 Python: A versatile and powerful programming language used for backend development.
  
- **Web Framework**:
  - Flask: A lightweight WSGI web application framework used to build the API.

- **Database**:
    - 🐬 MySQL: A popular open-source relational database system for storing and managing data.

- **ORM**:
  - SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.

- **Database Migration**:
  - Flask-Migrate: Handles SQLAlchemy database migrations for Flask applications using Alembic.

- **Authentication**:
  - Flask-JWT-Extended: Provides JSON Web Token (JWT) support for secure authentication and authorization.

- **API Documentation**:
  - Swagger: A tool for describing and visualizing RESTful APIs.

- **File Storage**:
  - Google Drive: Used for storing media files like images and videos of the exercises and users' profile pictures.

## File Structure

📂 Here’s a guide to the essential files and directories in our project:


- **`README.md`**: Overview of the project.
- **`LICENSE`**: MIT LICENSE
- **`.venv/`**: Python virtual environment
- **`Backend/`**: Contains the main source code.
  - **`app`**:  Entry point of the application.
  - **`api/v1/views**: A directory that contains all API 
endpoints
  - **`models/`**: A directory that contains files 
related to the table schemas of all entities
  - **`static/swagger.yaml`**: The API documentation
  - **`config.py`**: The flask configuration file
  - **`auth.py`**: API endpoints related to signup, login, and assigning routes.
  - **`google_api.py`**: A file continues all functions needed to manage files in Google Drive.
  - **`errors.py`**: Organize error handlers for the app
  - **`decorators.py`**: Decorators related to managing JWT token
  - **`credentials.json.enc`**:  Encrypted file containing the credentials needed to access Google Drive API
  - **`migrations/`**: Flask-migration and Alembic-related migration files and versions
 
- **`SetUp/`**: A directory that contains a bash script to set the needed environment variables and set the database
  - **`set_env.sh`**: Set up environment variables
  - **`setup_user_and_database.sh`**: Get Access to the local MySQL and create the database and the user
- **`exercises_data/`**: A directory that contains 2 Python scripts to manage to send a post request to the database at "http://localhost:5000/api/v1/exercises" and populate the exercises table
- **`requirements.txt`**: File contains all the dependencies needed by the Flask app

This map will help you navigate the project and locate key files with ease!

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Yasmin-tech/FitJourney.git
   cd FitJourney/
   ```
  
  2. Create and activate a virtual environment:
		```sh
		python3 -m venv .venv
		source .venv/bin/activate
		```

   3. Install the required dependencies:
	   ```sh
	   pip install -r requirements.txt
	   ```

   4. Modify the setup file, you'll need to open the file in your preferred text editor like Vim, and put in all the required information. *Read the comment in the file to guide you*
      ```sh
		vim SetUp/set_env.sh
      ```
<div align="center">
   <img src="https://i.imgur.com/LUvKQC7.png" alt="" />
  </div>

 5. After you fill your  variables in the `SetUp/set_env.sh` file, run
	```sh
	source SetUp/set_env.sh
	```
6. credentials.json :
	Decrypt the credentials.json.enc file, this contains the credentials for the Google Drive API of the app. This uses symmetric encryption, so you need the key used in the encryption process. 
	*please contact the Author to get access*
	 ```sh
	  cd Backend/
	  ./decrypt_credentials.sh <password>
	```
	*Replace `<password>` with the decryption password provided to you.*
	   
	Instead, follow the instructions in this video  [Link](https://www.youtube.com/watch?v=fkWM7A-MxR0&t=1163s) to create your own app and API key in Google Cloud
	**Now you can access credentials.json**
	[next step](#setting-up-the-database)


## Setting Up the Database

Now you are ready to set up the database. We'll start by creating the migration script to use for making any changes to the schema in the future.

-  **First-Time Setup**:
    
    -   If this is your first time running `Backend/app.py` or the migration script, the following will happen automatically:
        
        -   The script `SetUp/setup_user_and_database.sh` will run to create the database and the user for the first time.
            
        -   An admin user will be created using the email provided in `SetUp/set_env.sh`.
            
- **Subsequent Runs**:
    
    -   For subsequent runs of the app, `SetUp/setup_user_and_database.sh` will not run again.
        
    -   The admin user will already be present in the database, so no need to recreate it.


1. Database Migrations with Custom Directory:

	> NOTE:
	> The existing migration scripts are designed to bring an older schema to the current version. If your local schema already matches the latest version, running these migrations can cause conflicts. Solution: Creating and Using Your Own Migration Directory  To avoid these issues 👇

- Initialize Custom Migrations Directory:
	 Initialize a new migration directory with a custom name:
 ```sh
     flask db init --directory custom_migrations
   ```

- Create New Migrations in Custom Directory:
 IF making changes to your models, create new migration scripts in the custom directory:
 ```sh
     flask db migrate -m "description of changes" --directory custom_migrations
   ```
  
  - Apply Migrations from Custom Directory:
		 Apply the new migration scripts from the custom directory to your local database:
```sh
	flask db upgrade --directory custom_migrations
```
[next step](#running-swagger-documentation)


## Running Swagger Documentation

1.  **Run the Application**:
    
    -   First, ensure the application is running. Navigate to the backend directory and start the Flask application, make sure you are in the Backend directory:
                
        ```sh
        cd Backend
        ./app.py
        
        ```
        
2.  **Access Swagger Documentation**:
    
    -   Once the application is running, open your web browser and navigate to the following URL to access the Swagger documentation:
   
        ```sh
        http://localhost:5000/api/docs/
        ```

3. **Login with Admin User**:

    -   Log in as the admin user using the Swagger interface. Navigate to the `/admin/login` endpoint under the `auth` tag.
    
    -   Enter the admin credentials and execute the request. The response will include an access token.
    
    -   Use this access token to authorize yourself by clicking on the "Authorize" button in the Swagger interface and entering the token.
    
    -   With the access token, you can access other routes, such as `/users`, which are only accessible by users with Admin or Developer roles.
    
    -   Currently, you will find only one user, which is the admin itself.
    
    -   For more detailed information about the available endpoints and their responses, you can check in the Swagger documentation.


## Restarting the Server

After completing the initial setup, you don't need to repeat all the installation steps. For subsequent runs, you can simply follow these steps from the root directory:

1. **Activate the Virtual Environment**:
   ```sh
   source .venv/bin/activate
	```
2. **Set Environment Variables**:
	```sh
	source SetUp/set_env.sh
	```
3. **Navigate to Backend Directory and Start the Application**:
	```sh
	cd Backend
	./app.py
	```

## Populating Exercises Table with Predefined Exercises

To make use of the predefined dataset and populate the exercises table, follow these steps:

1.  **Ensure the Server is Running**:
    
    -   If you have stopped the server, restart it by following these commands from the root directory:
                
        ```sh
        source .venv/bin/activate
        source SetUp/set_env.sh
        cd Backend
        ./app.py
        
        ```
        
2.  **Open a New Terminal Tab**:
    
    -   Open a new terminal tab and navigate to the project directory.

3. **Activate the Virtual Environment**:

     ```sh
	 source .venv/bin/activate
    ```
        
4.  **Navigate to the exercises_data Directory**:
    
    -   Change to the `exercises_data` directory:
                
	```sh
	    cd exercises_data
	```
        
5.  **Uncomment the Last Line in the Script**:
    
    -   Open the `populate_exercises_table.py` script and uncomment the last line:
        
    <div align="center">
		   <img src="https://i.imgur.com/GZ8A0Z0.png" alt="" />
</div>
        
6.  **Pass the Admin JWT Access Token**:
    
    -   Make sure to pass the Admin JWT access token, which you can obtain from the `/admin/login` endpoint in the Swagger interface.
        
7.  **Run the Script to Populate Exercises Table**:
    
    -   Execute the script to read the `newExercisesDataset.csv` file and populate the exercises table line by line:
                
        ```sh
        ./populate_exercises_table.py <put here your admin access token>
        
        ```
        

**Exercise Planning Options**

Once the exercises table is populated, users have two options when planning their workout sessions:

- **Choose from Predefined Exercises**:
    
    -   Select exercises from the predefined list that has been populated in the exercises table.
        
-  **Create Custom Exercises**:
    
    -   Create their own custom set of exercises with detailed descriptions, images, and videos.
        

##### Additional Information

For more detailed information about the available endpoints and their responses, please refer to the Swagger documentation accessible at http://localhost:5000/api/docs/.

By following these steps, developers can easily populate the exercises table with the predefined dataset and provide users with flexible options for planning their workout sessions.


## Example of the end-user journey in the app

<div style="text-align: center;">
      <img src="https://i.imgur.com/TQfI2mr.png" alt="" />
    </div>



## Contributing


Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the Repository**: Click the "Fork" button at the top right of this page to create a copy of the repository under your GitHub account.
   
2. **Clone Your Fork**: Clone your forked repository to your local machine:
   ```sh
   git clone https://github.com/your-username/FitJourney.git
   cd FitJourney
   ```

3. **Create a New Branch:** Create a new branch for your feature or bug fix
	```sh
	git checkout -b feature/your-feature-name
	```
4. **Make Your Changes**: Make the necessary changes to the codebase. Ensure your code follows the project's coding standards and passes all tests.

5. **Commit Your Changes**: Commit your changes with a descriptive commit message:
	```sh
	git commit -m "Add your commit message here
	```
6. **Push to Your Fork:** Push your changes to your forked repository:
	```sh
	git push origin feature/your-feature-name
	```
7. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request. Provide a clear description of your changes and any related issue numbers.

We appreciate your contributions and thank you for improving the FitJourney APP API!

## Contact

 👤 For any questions, feedback, or inquiries, please contact:

- **Name**: Yasmin Mahmud
- **Email**: jazzsalam2020@gmail.com

We appreciate your interest in FitJourney and are here to help!

## License

 ©️This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

