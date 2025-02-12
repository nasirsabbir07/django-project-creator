import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up from scripts
APPS_DIR = os.path.join(BASE_DIR, "apps")
SETTINGS_FILE = os.path.join(BASE_DIR, "config", "settings", "base.py")


def create_app(app_name):
    """Creates django app in the apps directory with a structures layout"""

    # Ensure the apps directory exists
    if not os.path.exists(APPS_DIR):
        os.makedirs(APPS_DIR)

    # Define app path
    app_path = os.path.join(APPS_DIR, app_name)

    # Create the app directory
    os.makedirs(app_path, exist_ok=True)

    # Create the django app
    os.system(f"django-admin startapp {app_name} {app_path}")
    print(f"✅ Created Django app: {app_name}")

    # Remove default `tests.py`
    default_tests_file = os.path.join(app_path, "tests.py")
    if os.path.exists(default_tests_file):
        os.remove(default_tests_file)
        print(f"🚮 Removed default 'tests.py' from '{app_name}'")

    # Define custom folder structure
    custom_folders = [
        "tests/unit",
        "tests/integration",
    ]
    for folder in custom_folders:
        os.makedirs(os.path.join(app_path, folder), exist_ok=True)

    # Define initial files inside folders
    files_content = {
        "views.py": "from django.shortcuts import render\n\n",
        "serializers.py": "from rest_framework import serializers\n\n",
        "models.py": "from django.db import models\n\n",
        "tests/unit/__init__.py": "",
        "tests/integration/__init__.py": "",
        "urls.py": "from django.urls import path\n\nurlpatterns = []\n",
        "services.py": "",
        "utils.py": "",
    }

    # Create the files with default content
    for relative_path, content in files_content.items():
        file_path = os.path.join(app_path, relative_path)
        with open(file_path, "w") as f:
            f.write(content)

    print(f"📁 Created structured folders & files for '{app_name}'")

    # Auto-register the app in settings
    register_app_in_settings(app_name)


def register_app_in_settings(app_name):
    """Auto-registers the app in 'INSTALLED_APPS' inside settings/base.py."""

    if not os.path.exists(SETTINGS_FILE):
        print("⚠️ Settings file not found! Skipping auto-registration.")
        return

    with open(SETTINGS_FILE, "r") as f:
        settings_content = f.read()

    installed_apps_pattern = r"INSTALLED_APPS\s*=\s*\[([\s\S]*?)\]"
    match = re.search(installed_apps_pattern, settings_content)

    if match:
        installed_apps = match.group(1)
        if f"'apps.{app_name}'," not in installed_apps:
            new_installed_apps = installed_apps.strip() + f"\n    'apps.{app_name}',\n"
            updated_settings_content = settings_content.replace(installed_apps, new_installed_apps)

            with open(SETTINGS_FILE, "w") as f:
                f.write(updated_settings_content)

            print(f"✅ Auto-registered '{app_name}' in INSTALLED_APPS.")
        else:
            print(f"ℹ️ '{app_name}' is already registered in INSTALLED_APPS.")
    else:
        print("⚠️ Could not find INSTALLED_APPS in settings file!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_app(app_name)
