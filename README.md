# Image-Based Graphical Password Authentication System

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)

## Introduction

In today's digital landscape, the security of user accounts and data is of paramount importance. The Image-Based Graphical Password Authentication System is designed to provide a secure and user-friendly authentication method using Flask, PostgreSQL, and image-based graphical passwords.

Key Features:

- Secure image uploads and storage with PostgreSQL.
- Image-coordinate-based authentication for enhanced security.
- User-friendly authentication process, reducing the need for complex passwords.
- Robust security measures to protect user data.

## Getting Started

Follow these steps to set up and run the system locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/imonishkumar/Graphical_Password_Authentication_system_using_flask
   cd Graphical_Password_Authentication_system_using_flask
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the PostgreSQL Database:**

   - Configure the database connection in `app.py`:

     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
     ```

   - Initialize and upgrade the database:

     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

4. **Run the Flask Application:**

   ```bash
   flask run
   ```

5. **Access the Application:**

   Open your web browser and visit http://localhost:5000 to use the application.

## Usage

1. **User Registration:**

   - Register an account by providing a username, email, and uploading an image.
   - During registration, select specific image coordinates to create a unique authentication pattern.

2. **Login and Authentication:**

   - Log in using your registered email.
   - You'll be prompted to enter the image coordinates based on your predefined pattern.
   - The system will authenticate you based on the entered coordinates.

## Security Measures

This system incorporates several security measures:

- Secure storage of image data as binary, reducing the risk of unauthorized access.
- Tolerance range during authentication to account for small variations.
- Unique image-coordinate pattern for each user, making replication difficult for attackers.

## Password Reset Functionality

The system also provides a password reset feature:

- Users can request a password reset link via email.
- Password reset links are valid for a limited time.
- The system sends a link to the user's email address for resetting their password.

## Contributing

Contributions to this project are welcome. You can contribute by opening issues, providing feedback, or submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or collaboration opportunities, feel free to contact us mail at monishkumarpecai@gmail.com.

---

*Note: Replace `username:password@localhost/database_name` in the database configuration with your actual database credentials.*
```
