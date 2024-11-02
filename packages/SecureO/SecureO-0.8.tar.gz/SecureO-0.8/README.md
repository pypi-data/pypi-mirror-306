# Hi, I'm Yash Jain!

## About Me

I am a Full Stack Web Developer and a Python Developer. Click the link for my complete [@PortFolio](https://portfolio-86j1.onrender.com/)

## Links

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://portfolio-86j1.onrender.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yash-jain-47b043276/)

# SecureO

SecureO is a command-line password manager built to securely store, manage, and retrieve your passwords. It includes features for generating strong passwords, managing user access, and securely saving password entries.

## Features

- Secure Password Storage: Passwords are stored with secure encryption, ensuring safety.
- Password Strength Verification: Passwords are evaluated for strength.
- Password Generation: Generates strong, randomized passwords if needed.
- User Management: Multiple users can manage and store their passwords in separate accounts.

## Tech Stack

**Client:** Python, Command Line Interface

**Server:** MongoDB

## Installation

Install SecureO with pip

```bash
  pip install SecureO
  pm
```

After installing, SecureO provides a pm command for accessing the password manager via the command line. However, if pm does not work immediately, it may be because the Python Scripts directory is not in your system PATH.

#### Follow the steps below to add the Scripts folder to your PATH.

    Step 1 - Locate the Scripts Folder: C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python<YourPythonVersion>\Scripts\
    Step 2 - Add to PATH:
      1. Go to System Properties > Advanced > Environment Variables.
      2. Under System Variables, find the Path variable and click Edit.
      3. Add the path to your Scripts folder from step 1.

## Commands

#### Display all available commands and their usage.

```http
  pm help
```

#### Register a new user

```http
  pm set user
```

You will be prompted to enter a unique username and a password for the account. If the entered password does not meet strength requirements, you will be given the option to regenerate or improve it.

#### Log into an existing user account.

```http
  pm get user <username>
```

You will need to enter the password associated with the specified username to log in.

#### Save a password entry to your account.

```http
  pm save password
```

You will be prompted to enter a name and the password to save. SecureO can generate a strong password for you if needed.

#### View all saved passwords in your account.

```http
  pm view password
```

#### Delete a password entry by specifying its ID.

```http
  pm del password <password_id>
```

#### Edit a password entry by specifying its ID.

```http
  pm edit password <password_id>
```

#### Clear the screen in the SecureO CLI.

```http
  pm clear
```

#### Exit the SecureO CLI.

```http
  pm exit
```

## Authors

- [@Yash Jain](https://www.github.com/yash-k-jain)

- [@Aryan Sagar](https://www.linkedin.com/in/aryan-sagar-6b75651b6/)

## Acknowledgements

- [PyPI](https://pypi.org/)
- [Stack OverFlow](https://stackoverflow.com/)

## Appendix

It uses ceaser ciapher algorithm in order to save the password in the backend database.

## FAQ

#### Question 1 Why pm command is not working after installation?

Answer 1 The main reason is that your system path variable does not involve the path for your Script path folder.

#### Question 2 How to know the password manager works?

Answer 2 Run pm help after running pm command.

## Support

For support, email yash.test.project@gmail.com.

## Feedback

If you have any feedback, please reach out to us at yash.test.project@gmail.com

## Badges

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
