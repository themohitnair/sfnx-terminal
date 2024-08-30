from typer import Typer
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import getpass
from art import text2art
from sfnx.db import init_db, get_session, verify_user_master_password, check_exists, configure
from sfnx.security import encrypt, decrypt, derive_key

app = Typer()
console = Console()

@app.command()
def init():

    rules = [
        ("Rule 1:", "The master password is the prime password which you will be using to access all your passwords in sfnx. Forgetting it means irreversibly losing access to all your other passwords. Always remember it."),
        ("Rule 2:", "Creating an easy-to-remember password doesn't mean making it short and weak. It is better to follow this for all passwords you store in this password manager."),
        ("Rule 3:", "Your master password must have at least 15 characters. It is recommended to use a long passphrase; for example: \"myc@tn@medg@mbitst@rtedthes0vietunion@ccident@lly\""),
    ]

    rules_text = "\n".join([f"{rule} {point}" for rule, point in rules])
    panel_content = Text(rules_text, style="cyan")
    
    console.print(Panel(panel_content, title="Important Rules", expand=False))
    
    master_password = getpass.getpass("Enter the master password you wish to use: ")
    confirm = getpass.getpass("Enter the password again [confirm]: ")

    if confirm != master_password:
        console.print("[bold red]Error:[/bold red] Passwords do not match. Please try again.", style="bold red")
        return    

    name = input("Enter your name or alias [required]: ")

    key = derive_key(master_password)
    encrypted_secret = encrypt(key, name)

    
    console.print("\nThank you for setting up sfnx!", style="bold green")
    init_db



if __name__ == "__main__":
    app()
