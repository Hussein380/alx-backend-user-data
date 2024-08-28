
```markdown
# Password Encryption Module

This module provides functionality for securely hashing and validating passwords using the `bcrypt` library. 

## Installation

Ensure you have `bcrypt` installed. You can install it using pip:

```bash
pip install bcrypt
```

## Usage

### Hashing Passwords

To hash a password, use the `hash_password` function. It takes a plaintext password as input and returns a hashed password in bytes.

Example:

```python
from encrypt_password import hash_password

password = "MyAmazingPassw0rd"
hashed_password = hash_password(password)
print(hashed_password)
```

### Validating Passwords

To check if a plaintext password matches a hashed password, use the `is_valid` function. It takes the hashed password and the plaintext password as arguments, and returns `True` if the password matches, otherwise `False`.

Example:

```python
from encrypt_password import is_valid, hash_password

password = "MyAmazingPassw0rd"
hashed_password = hash_password(password)
print(is_valid(hashed_password, password))  # True
```

## Functions

### `hash_password(password: str) -> bytes`

Hashes a plaintext password using a randomly generated salt.

- **Parameters**: `password` (str) - The plaintext password to hash.
- **Returns**: `bytes` - The hashed password.

### `is_valid(hashed_password: bytes, password: str) -> bool`

Checks if the given plaintext password matches the hashed password.

- **Parameters**:
  - `hashed_password` (bytes) - The hashed password.
  - `password` (str) - The plaintext password to check.
- **Returns**: `bool` - `True` if the password matches, otherwise `False`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository and submit pull requests. For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY).

## Acknowledgements

- [bcrypt](https://pypi.org/project/bcrypt/) for secure password hashing.
