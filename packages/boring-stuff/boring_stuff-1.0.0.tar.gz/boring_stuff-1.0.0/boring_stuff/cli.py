import argparse
import shutil
import os
from importlib import resources

def copy_template(template_name):
    try:
        # Use `importlib.resources` to open the path within the package
        with resources.path("boring_stuff.templates", template_name) as src_dir:
            dest_dir = os.getcwd()
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
            print(f"Successfully created {template_name} project structure.")
    except Exception as e:
        print(f"Error creating project structure: {e}")

def start():
    print("Select your project type:")
    print("1. Flask")
    print("2. Django (not implemented)")
    print("3. FastAPI")
    print("4. Django+DRF (not implemented)")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("Setting up Flask project...")
        copy_template("flask")
    elif choice == "3":
        print("Setting up FastAPI project...")
        copy_template("fastapi")
    else:
        print("Option not implemented yet.")

def main():
    parser = argparse.ArgumentParser(prog="boring-stuff")
    subparsers = parser.add_subparsers(dest="command")

    # Define the `start` subcommand
    start_parser = subparsers.add_parser("start", help="Start the project setup")
    start_parser.set_defaults(func=start)

    args = parser.parse_args()
    if args.command:
        args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
