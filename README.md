# sfnx

`sfnx` is a minimal terminal-based password manager built using Python. It leverages the `Typer` CLI framework, `SQLModel` for database management, `Argon2` for key derivation, `AES` for encryption, and `SQLite` for storage.

## Features

- **Master Password**: Secure your password database with a single master password.
- **Encrypted Storage**: All passwords are encrypted using AES with a 256-bit key derived from your master password.
- **Simple Commands**: Easily initialize, add, delete, and view passwords from the terminal.

## Installation
### Arch Linux Install
   ```sh
   yay -Ss sfnx
   ```

   Obviously, other package managers such as aura, trizen, and paru can be used.

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

4. **`copypass`**:  
   - Retrieves and decrypts passwords for a specified service and username.
   - Displays the decrypted password in the terminal.

   Example:
   ```sh
   sfnx copypass
   ```

5. **`afresh`**
   - Deletes the password database from your system and hence your current configuration along with it
   - In order to use the utility after this command, you must use `sfnx init` to reconfigure the command-line application
   - The `afresh` command is irreversible. Proceed with caution when using the command

   Example:
   ```sh
   sfnx afresh
   ```

6. **`modpass`**
   - Updates the username/password attributes (and hence the stored salt) according to the user's choice.
   
   Example:
   ```sh
   sfnx modpass
   ```

7. **`services`**
   - Shows services along with usernames stored in the database.

   Examples:
   ```sh
   sfnx services
   ```

8. **`--help`**:  
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

3. **Retrieving Passwords**: With `sfnx copypass`, the stored encrypted password is decrypted and copied to your clipboard after verifying the master password.

4. **Deleting Passwords**: The `sfnx delpass` command removes the password entry corresponding to the service and username, provided the correct master password is entered.

5. **Updating Passwords**: The `sfnx modpass` command updates the password entry corresponding to the service and username, provided the correct master password is entered.

6. **Viewing added entries**: For convenience, the `sfnx services` command shows all the services and list of usernames for each service (not the passwords), so that the user can view the passwords that they entered and proceed with other entries without being confused about the ones already added.

## Repository

For more details, check out the [GitHub repository](https://github.com/themohitnair/sfnx).

- [LICENSE](https://github.com/themohitnair/sfnx/blob/main/LICENSE)