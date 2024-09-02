```markdown
# Basic Authentication Project

## Overview

This project focuses on implementing Basic Authentication for a simple API to understand the authentication process and Base64 encoding. The goal is to learn the fundamentals of Basic Authentication by developing it manually, which is typically handled by libraries or frameworks in production environments.

## Project Details

- **Project Name:** Basic Authentication
- **Specialization:** Back-end
- **Average Score:** 102.69%
- **Project Duration:** September 2, 2024 (6:00 AM) - September 4, 2024 (6:00 AM)
- **Checker Release Date:** September 2, 2024 (6:00 PM)
- **Auto Review Deadline:** At the end of the project period

## Background Context

In this project, you will:
- Implement Basic Authentication on a simple API.
- Learn what authentication means, what Base64 is, and how to use it.
- Understand how to send the Authorization header in HTTP requests.

## Learning Objectives

By the end of this project, you should be able to:
- Explain what authentication means.
- Describe Base64 encoding and how to encode a string in Base64.
- Understand Basic Authentication and how to send the Authorization header.

## Requirements

- **Python Version:** 3.7
- **Operating System:** Ubuntu 18.04 LTS
- **File Requirements:**
  - Files should end with a new line.
  - The first line of all files should be exactly `#!/usr/bin/env python3`.
  - Code should use the `pycodestyle` style (version 2.5).
  - All files must be executable.
  - Documentation should be provided for all modules, classes, and functions.

## Tasks

1. **Simple-basic-API**: 
   - Set up and start the server.
   - Test the API using curl commands.

2. **Error Handler: Unauthorized**
   - Add an error handler for 401 Unauthorized status code.
   - Create a new endpoint to test this error handler.

3. **Error Handler: Forbidden**
   - Add an error handler for 403 Forbidden status code.
   - Create a new endpoint to test this error handler.

4. **Auth Class**
   - Create an `Auth` class with methods for authentication.
   - Implement the `require_auth`, `authorization_header`, and `current_user` methods.

5. **Define Routes That Don't Need Authentication**
   - Update the `require_auth` method to handle excluded paths.

6. **Request Validation**
   - Validate requests and handle errors based on authentication status.

7. **Basic Auth**
   - Create a `BasicAuth` class that inherits from `Auth`.
   - Update the app to use `BasicAuth` based on the `AUTH_TYPE` environment variable.

8. **Basic - Base64 Part**
   - Add methods to handle Base64 encoding and decoding in the `BasicAuth` class.

## Usage

To set up and run the server:

```bash
pip3 install -r requirements.txt
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

To test the API endpoints:

```bash
curl "http://0.0.0.0:5000/api/v1/status"
curl "http://0.0.0.0:5000/api/v1/unauthorized"
curl "http://0.0.0.0:5000/api/v1/forbidden"
```

## Repository

- **GitHub Repository:** [alx-backend-user-data](https://github.com/your-repo/alx-backend-user-data)
- **Directory:** `0x01-Basic_authentication`
- **Files:** `api/v1/app.py`, `api/v1/views/index.py`, `api/v1/auth/auth.py`, `api/v1/auth/basic_auth.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask documentation and tutorials
- Python Base64 encoding references
- REST API authentication resources

```
