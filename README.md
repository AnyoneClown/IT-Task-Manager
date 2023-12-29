# Task Manager Project

Welcome to the Task Manager project! This web application provides a platform for managing tasks and user accounts. Below is an overview of the implemented features:

## Deployed Website
Explore the deployed Task Manager web application on [Render](https://it-task-manager-5z1u.onrender.com/)! You can use test profile for this or create your own on registration page! 
### Username: Testing | Password: test12345

## User Features:

### Registration
New users can register for an account.

### Change Password, Delete Account
Users have the ability to change their password and delete their account. These actions are restricted to the account owner.

### Update Account Information
Users can update their account information, but only the account owner has this privilege.

### User Profiles
Each user has their own profile where they can view and manage their information.

## Task Features:

### Create, Update, and Delete Tasks
Users can create new tasks, update existing tasks, and delete tasks. Task creation includes the ability to specify participants, task type, and other details.

### Task Tabs
Each user has access to tabs for "My Completed Tasks" and "My Tasks in Progress."

### Task Types
Users can create new task types to categorize tasks effectively.

## Developer Positions

### Create New Positions
Administrators can create new positions for developers, specifying roles and responsibilities.

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Apply database migrations with `python manage.py migrate`.
4. Start the development server with `python manage.py runserver`.

## Contributing

If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test your changes thoroughly.
5. Submit a pull request.
