# sfnx

`sfnxterm` or `sfnx` is a minimal terminal-based password manager built using Python. It leverages the `Typer` CLI framework, `SQLModel` for database management, `Argon2` for key derivation, `AES` for encryption, and `SQLite` for storage.

## Features

- **Master Password**: Secure your password database with a single master password.
- **Encrypted Storage**: All passwords are encrypted using AES with a 256-bit key derived from your master password.
- **Simple Commands**: Easily initialize, add, delete, and view passwords from the terminal.

## Installation

To install `sfnx-terminal`, use `pipx` to manage a global environment on your Linux machine:

```sh
sudo pacman -S pipx
pipx install sfnx
pipx ensure path
source ~/.bashrc
```

## Usage

### Commands

1. **`init`**:  
   - Initializes the password manager.
   - Prompts for a master password and a verification secret (e.g., your name or alias).
   - Stores the encrypted verification secret in the database.
   - If the database is already initialized, this command acts as a test to verify the master password.

   Example:
   ```sh
   sfnx init
   ```

2. **`addpass`**:  
   - Adds a new password to the encrypted database.
   - Requires a service name, username, and the password to store.
   - Passwords are encrypted with AES before being stored.

   Example:
   ```sh
   sfnx addpass
   ```

3. **`delpass`**:  
   - Deletes a password for a specific service and username combination.
   - Requires the master password for verification.

   Example:
   ```sh
   sfnx delpass
   ```

4. **`viewpass`**:  
   - Retrieves and decrypts passwords for a specified service and username.
   - Displays the decrypted password in the terminal.

   Example:
   ```sh
   sfnx viewpass
   ```

5. **`--help`**:  
   - Displays help information for the commands.

   Example:
   ```sh
   sfnx --help
   ```

### Security

- **Key Derivation**: The master password is processed using `Argon2`, a memory-hard key derivation function. This adds security against brute-force attacks.
  ```python
  key = low_level.hash_secret_raw(
      m_password.encode(),
      salt,
      time_cost=2,
      memory_cost=102400,
      parallelism=8,
      hash_len=32,
      type=Type.ID
  )
  ```
- **Encryption**: Passwords are encrypted using AES in CBC mode with PKCS7 padding. The encryption key is derived from the master password.
  ```python
  cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
  ```
- **Database**: Passwords and secrets are stored in an SQLite database, with each record containing the service name, username, encrypted password, and a unique salt.

### Workflow

1. **Initialization**: On running `sfnx init`, the database is created and configured with the master password and verification secret. This configuration is stored securely using encryption.

2. **Adding Passwords**: When adding a password with `sfnx addpass`, the password is encrypted with AES, using a key derived from the master password and a unique salt.

3. **Retrieving Passwords**: With `sfnx viewpass`, the stored encrypted password is decrypted and displayed after verifying the master password.

4. **Deleting Passwords**: The `sfnx delpass` command removes the password entry corresponding to the service and username, provided the correct master password is entered.

## Repository

For more details, check out the [GitHub repository](https://github.com/themohitnair/sfnxterm).

- [LICENSE](https://github.com/themohitnair/sfnxterm/blob/main/LICENSE)

- [PyPI registry](https://pypi.org/project/sfnx/)