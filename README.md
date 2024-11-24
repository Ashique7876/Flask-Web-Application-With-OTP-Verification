
#  Flask OTP Verification Web Application

## Description
This Flask-based web application allows users to register, receive a One-Time Password (OTP) via email, and verify their identity by entering the OTP. The application includes user authentication, email-based registration verification, and a protected dashboard for logged-in users. The OTP has a time-sensitive validity period, enhancing security.

## Key Features
 ### 1.User Registration with OTP Verification:
Users register with a username, email, and password. An OTP is sent to the registered email for verification.
### 2.OTP Expiration:
OTPs expire after 2 minutes. Expired OTPs require users to re-register or request a new OTP.
### 3.User Login:
After OTP verification, users can log in using their email and password.

## Technologies Used
### Frontend
HTML5: Markup for structure.
CSS: Styling, including responsive design.
JavaScript: Form validation and interactivity.

### Backend
Python: Core logic and application structure.
Flask: Framework for routing, session management, and backend logic.

### Database
SQLite : Lightweight database for storing user and OTP data.

## Installation and Usage Instructions
### Prerequisites
1.Python 3.x installed on your machine.
2.Installed pip for managing Python dependencies.

## Installation Steps
### 1.Clone the Repository:
git clone cd 

### 2.Install Python Dependencies:
Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-Mail==0.9.1 Werkzeug==3.0.4 

### 3.Set Up Database:
The database is automatically initialized when the application runs for the first time. No manual setup is required.

### 4.Configure Email for OTP (Gmail):

Use a Gmail account for sending OTPs.
Enable App Passwords in Gmail for secure email sending.
Update MAIL_USERNAME and MAIL_PASSWORD in the application:

app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'


## Usage

Run the Application:
Start the Flask server by executing:

python app.py
Access the Application:
Open a web browser and navigate to http://127.0.0.1:5000.

Register a New User:

Enter a username, email, and password.
An OTP will be sent to the provided email.
Verify OTP:
Enter the received OTP to complete registration.

Login:

Use the registered email and password to log in.
Access the user dashboard.
Logout:
Click the logout button to end the session.


## Screen Short

![Register Page](https://github.com/user-attachments/assets/b2bf3a2f-aeb0-495a-9317-16453597ff3a)
![Login Page](https://github.com/user-attachments/assets/3fea24a3-4a7d-4fa9-80e8-5fa2085d8786)
![Login Page](https://github.com/user-attachments/assets/6f1e1416-5fb3-449f-86d2-632dfa0b58e7)
![Home Page](https://github.com/user-attachments/assets/f9ecd341-6bce-4612-ac6c-d88a0f284348)




