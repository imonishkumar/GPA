# Image-Based Graphical Password Authentication System

Secure and user-friendly authentication system using Flask, PostgreSQL, and image-based graphical passwords.

## Introduction

In today's digital landscape, the security of user accounts and data is of paramount importance. This project presents a secure image upload and authentication system, leveraging the Flask framework. This authentication approach uses image coordinates instead of traditional text-based passwords to enhance security and user experience.

Key features of this system include:

- Secure image uploads with PostgreSQL storage.
- Image-coordinate-based authentication for improved security.
- User-friendly authentication method, reducing the need for complex passwords.
- Robust security measures to protect user data.

## Getting Started

Follow these steps to set up and run the system locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/imonishkumar/Graphical_Password_Authentication_system_using_flask
   cd Graphical_Password_Authentication_system_using_flask
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up a PostgreSQL database. Update the database configuration in `app.py`:

   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
   ```

4. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the Flask application:

   ```bash
   flask run
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Register an account by providing a username, email, and uploading an image.
2. During registration, select specific image coordinates to create a unique authentication pattern.
3. Log in using your email, and you'll be prompted to enter the coordinates based on your predefined pattern.
4. The system will authenticate you based on the entered coordinates.

## Security Measures

This system employs several security measures:

- Image data is securely stored as binary data, reducing the risk of unauthorized access.
- A tolerance range is used during authentication to account for small variations.
- The image-coordinate pattern is unique to each user, making it challenging for attackers to replicate.

## Contributing

Contributions to this project are welcome. You can contribute by opening issues, providing feedback, or submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or collaboration opportunities, feel free to contact us at monishkumarpecai@gmail.com

```

