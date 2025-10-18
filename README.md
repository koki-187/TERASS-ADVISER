# TERASS - User Registration System

A simple and secure user registration and authentication web application built with Flask.

## Features

- **User Registration**: Create new user accounts with username, email, and password
- **Secure Password Storage**: Passwords are hashed using industry-standard algorithms
- **Input Validation**: Comprehensive validation for user inputs
- **User Authentication**: Login system with session management
- **Responsive Design**: Modern, mobile-friendly interface
- **Flash Messages**: User-friendly feedback for all actions

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/koki-187/TERASS-.git
cd TERASS-
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

For development with debug mode:
```bash
export FLASK_DEBUG=true
python app.py
```

For production, set a secure secret key:
```bash
export SECRET_KEY='your-secure-random-secret-key'
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. You will be redirected to the login page. Click "Register here" to create a new account.

4. Fill in the registration form:
   - Username (must be unique)
   - Email (must be unique)
   - Password (minimum 6 characters)
   - Confirm Password

5. After successful registration, you can login with your credentials.

## Project Structure

```
TERASS-/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── register.html    # Registration page
│   ├── login.html       # Login page
│   └── dashboard.html   # User dashboard
└── static/              # Static files
    └── css/
        └── style.css    # Stylesheet
```

## Security Features

- Password hashing using Werkzeug's security utilities
- Session-based authentication
- Input validation and sanitization
- Protection against SQL injection using parameterized queries
- CSRF protection through Flask's built-in mechanisms

## Technologies Used

- **Flask**: Web framework
- **SQLite**: Database
- **Werkzeug**: Password hashing
- **HTML/CSS**: Frontend
- **Jinja2**: Template engine

## Production Deployment

**Important Security Notes for Production:**

1. **Secret Key**: Always set a secure SECRET_KEY environment variable:
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

2. **Database**: Consider using PostgreSQL or MySQL instead of SQLite for production.

3. **HTTPS**: Always use HTTPS in production to protect user credentials.

4. **Additional Security**: Consider implementing:
   - Rate limiting for login/registration attempts
   - Email verification
   - CAPTCHA for registration
   - Two-factor authentication
   - More robust email validation (e.g., using `email-validator` library)

5. **Web Server**: Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

For more information, visit: https://www.genspark.ai/spark?id=d76d3c30-5936-45ef-8267-10818d137495