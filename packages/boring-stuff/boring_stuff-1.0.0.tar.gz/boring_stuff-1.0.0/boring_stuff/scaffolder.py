import os
import shutil
from pathlib import Path


def copy_template(template_dir, project_name):
    dest_path = Path.cwd() / project_name
    shutil.copytree(template_dir, dest_path)
    print(f"Project created at {dest_path}")


def create_project(project_type, project_name):
    templates_dir = Path(__file__).parent / "templates" / project_type
    if templates_dir.exists():
        copy_template(templates_dir, project_name)
    else:
        print(f"No template found for project type: {project_type}")
