from typer import Typer
from rich.console import Console
from rich.text import Text
import pyperclip
from rich.panel import Panel
import getpass
import os
from sfnx.db import init_db, verify_user_master_password, check_db_exists, configure, get_user_name, add_password, retrieve_password, delete_password
from sfnx.security import encrypt, decrypt, derive_key

app = Typer()
console = Console()

rules = [
    ("Rule 1:", "The master password is the prime password which you will be using to access all your passwords in sfnx. Forgetting it means irreversibly losing access to all your other passwords. Always remember it."),
    ("Rule 2:", "Creating an easy-to-remember password doesn't mean making it short and weak. It is better to follow this for all passwords you store in this password manager."),
    ("Rule 3:", "Your master password must have at least 15 characters. It is recommended to use a long passphrase; for example: \"myc@tn@medg@mbitst@rtedthes0vietunion@ccident@lly\""),
]

@app.command("init")
def init():
    """
    Initialize the password manager and set up the master password.

    This command will guide you through setting up your master password and configuring
    your password manager. Ensure you remember your master password as it is crucial
    for accessing your stored passwords.
    """
    try:
        if not check_db_exists():
            rules_text = "\n".join([f"{rule} {point}" for rule, point in rules])
            panel_content = Text(rules_text, style="cyan")
            console.print(Panel(panel_content, title="Important Rules", expand=False))

            master_password = getpass.getpass("Enter the master password you wish to use: ")
            confirm = getpass.getpass("Enter the password again [confirm]: ")

            if confirm != master_password:
                console.print("[bold red]Error:[/bold red] Passwords do not match. Please try again.", style="bold red")
                return

            name = input("Enter your name or alias [required]: ")
            console.print(f"\nThank you for setting up sfnx, {name}!", style="bold green")
            salt = os.urandom(16)
            key = derive_key(master_password, salt)
            encrypted_secret = encrypt(key, name)
            configure(master_password, name)
        else:
            print("This is a configuration test to see if you have setup your password manager properly. See sfnx --help for more details.")
            master_password_attempt = getpass.getpass("Enter your master password: ")
            if verify_user_master_password(master_password_attempt):
                username = get_user_name(master_password_attempt)
                print(f"Welcome, {username}!")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")

@app.command("addpass")
def addpass():
    """
    Add a new password entry for a service.

    This command allows you to add a new password entry for a specific service
    by providing the service name, username, and password. Make sure to enter
    the password correctly and confirm it before saving.
    """
    try:
        if not check_db_exists():
            init()
        else:
            service = input("Enter the name of the service: ")
            username = input("Enter the username used for the service: ")
            password = getpass.getpass("Enter the password used for this service and username: ")
            c_password = getpass.getpass("Enter the above password again for confirmation: ")
            if password == c_password:
                master_password_attempt = getpass.getpass("Enter your master password: ")
                add_password(master_password_attempt, service, username, password)
            else:
                console.print("[bold red]Error:[/bold red] Passwords do not match. Please try again.", style="bold red")
                return
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")

@app.command("delpass")
def delpass():
    """
    Delete a password entry for a service.

    This command removes a stored password entry for a specific service based on
    the provided service name and username. You will need to provide your master
    password to confirm the deletion.
    """
    try:
        if not check_db_exists():
            init()
        else:
            service = input("Enter the name of the service: ")
            username = input("Enter the username used for the service: ")
            master_password_attempt = getpass.getpass("Enter your master password: ")
            delete_password(master_password_attempt, service, username)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")

@app.command("copypass")
def copypass():
    """
    Copy a password entry for a service.

    This command retrieves and copies a password entry for a specific service
    to the clipboard. You need to provide the service name, username, and your
    master password. The password will be copied to the clipboard for your convenience.
    """
    try:
        if not check_db_exists():
            init()
        else:
            service = input("Enter the name of the service: ")
            username = input("Enter the username used for the service: ")
            master_password_attempt = getpass.getpass("Enter your master password: ")
            password = retrieve_password(master_password_attempt, service, username)
            if password:
                pyperclip.copy(password)
                console.print("[bold green]Password copied to clipboard.[/bold green]", style="bold green")
            else:
                console.print("[bold red]Error:[/bold red] Password not found.", style="bold red")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")

@app.command("afresh")
def afresh():
    """
    Delete the sfnx.db file and reset the configuration.

    This command will remove the sfnx.db file, effectively deleting all stored
    passwords and configuration. This action is irreversible, so make sure
    you really want to reset everything before running this command.
    """
    try:
        if check_db_exists():
            confirm = input("Are you sure you want to delete the sfnx.db file and reset all configurations? [y/N]: ").lower()
            if confirm == 'y':
                os.remove("sfnx.db")
                console.print("[bold green]Database file deleted and configuration reset.[/bold green]", style="bold green")
            else:
                console.print("[bold yellow]Operation cancelled.[/bold yellow]", style="bold yellow")
        else:
            console.print("[bold red]Error:[/bold red] Database file does not exist.", style="bold red")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")

if __name__ == "__main__":
    app()