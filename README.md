# Van Rental Manager

[Video Demo](#) <!-- Replace with your video demo URL -->

## Description

The Van Rental Manager is a web application designed to help users manage their van rental business efficiently. It allows users to register an account, log in, add, update, and delete rental entries, and view a list of their current rentals. The application provides a user-friendly interface for managing rental details such as rental dates, client contacts, pickup locations, destinations, and agreed prices. It also includes email notifications to enhance user experience and keep users informed.

## Features

- **User Registration**: Users can register for a new account by providing a username, password, email, and optional phone number. Passwords are securely hashed before being stored in the database. Upon successful registration, users receive a welcome email.

- **User Authentication**: Registered users can log in using their username and password. Passwords are hashed and compared with the stored hash for authentication.

- **Session Management**: User sessions are managed using Flask's session management. Upon successful login, the user's ID is stored in the session, allowing them to access protected routes. Users receive a login notification email upon successful login.

- **Rental Management**: Authenticated users can add, update, and delete rental entries. Each rental entry includes details such as rental dates, client contacts, pickup locations, destinations, and agreed prices.

- **List View of Rentals**: Users can view a list of their current rentals, sorted by creation date. The list displays rental IDs, rental dates, client contacts, destinations, and agreed prices.

- **Email Notifications**: Users receive email notifications for:
  - **Registration**: A welcome email upon successful registration.
  - **Login**: A notification email upon successful login.
  - **Upcoming Rentals**: Reminders about upcoming rentals, sent 24 hours before the scheduled rental.

## File Structure

- **`__init__.py`**: Initializes the Flask application and registers blueprints.
- **`auth.py`**: Contains routes and functions related to user authentication, including registration, login, logout, and session management.
- **`db.py`**: Defines functions for interacting with the SQLite database, including database initialization, getting the database connection, and closing the connection.
- **`schema.sql`**: Defines the database schema, including tables for users and van rental entries.
- **`van_manager.py`**: Contains routes and functions related to van rental management, including adding, updating, and deleting rental entries.
- **`email_notifications.py`**: Handles sending email notifications for registration, login, and upcoming rentals.
- **`templates/`**: Directory containing HTML templates for user interface components.
  - **`base.html`**: Base template with common elements such as header, navigation, and flash messages.
  - **`auth/`**: Directory containing templates for authentication-related pages.
    - **`login.html`**: Template for the login page.
    - **`register.html`**: Template for the registration page.
  - **`van_manager/`**: Directory containing templates for van rental management pages.
    - **`add_rental.html`**: Template for adding a new rental entry.
    - **`rentals.html`**: Template for displaying a list of rental entries.
    - **`update_rental.html`**: Template for updating an existing rental entry.
- **`static/`**: Directory containing static assets such as CSS files.

## Design Choices

- **Flask Framework**: Flask was chosen for its simplicity and flexibility, allowing for rapid development of web applications.
- **SQLite Database**: SQLite was chosen as the database management system for its ease of use and suitability for small-scale applications.
- **Session-Based Authentication**: Session-based authentication was implemented for its simplicity and security benefits compared to storing passwords in cookies.
- **Email Notifications**: Email notifications were added to enhance user engagement and provide timely reminders and updates.
- **Separation of Concerns**: Routes, database operations, and HTML templates are organized into separate files and directories for better code maintainability and scalability.

This README provides an overview of the Van Rental Manager project, including its features, file structure, and design choices. For detailed instructions on setting up and running the application, please refer to the project documentation or contact the developer.
