import argparse
import json
import os
import secrets
import shutil
import string
import subprocess
import sys


def generate_secret_key():
    """Generates a secure Django SECRET_KEY."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(chars) for _ in range(50))


def create_folders(base_dir):
    folders = [
        f"{base_dir}/apps",
        f"{base_dir}/config",
        f"{base_dir}/config/settings",
        f"{base_dir}/config/middleware",
        f"{base_dir}/config/decorators",
        f"{base_dir}/config/logging",
        f"{base_dir}/config/exceptions",
        f"{base_dir}/config/utils",
        f"{base_dir}/static",
        f"{base_dir}/templates",
        f"{base_dir}/media",
        f"{base_dir}/logs",
        f"{base_dir}/scripts",
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ Folder structure created.")


def create_files(base_dir, secret_key):
    files = {
        f"{base_dir}/requirements.txt": """Django==5.1.5
djangorestframework==3.15.2
python-dotenv==1.0.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
""",
        f"{base_dir}/.gitignore": ".venv/\n__pycache__/\n*.pyc\nlogs/\nmedia/\n.env\n.vscode\n.idea\n",
        f"{base_dir}/config/.env": f"""
SECRET_KEY={secret_key}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=dev  # Add this line to specify the environment, Change this to 'prod' or 'staging' for different environments
DATABASE_URL_DEV=postgres://user:password@localhost:5432/dev_db
DATABASE_URL_STAGING=postgres://user:password@localhost:5432/staging_db
DATABASE_URL_PROD=postgres://user:password@localhost:5432/prod_db
DJANGO_SETTINGS_MODULE=config.settings.dev
""",
        f"{base_dir}/config/settings/base.py": """
import os
from pathlib import Path
import dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv.load_dotenv(BASE_DIR / "config" / ".env")


SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Determine the environment and use the appropriate database URL
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

if ENVIRONMENT == 'prod':
    DATABASE_URL = os.getenv('DATABASE_URL_PROD')
elif ENVIRONMENT == 'staging':
    DATABASE_URL = os.getenv('DATABASE_URL_STAGING')
else:  # Default to development
    DATABASE_URL = os.getenv('DATABASE_URL_DEV')

# Fallback to SQLite if no valid DATABASE_URL is provided
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=False) or {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
        f"{base_dir}/config/settings/dev.py": "from .base import *\nDEBUG = True\n",
        f"{base_dir}/config/settings/prod.py": "from .base import *\nDEBUG = False\nALLOWED_HOSTS = ['yourdomain.com']\n",
        f"{base_dir}/config/settings/staging.py": "from .base import *\nDEBUG = False\nALLOWED_HOSTS = ['staging.yourdomain.com']\n",
    }
    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)
    print("✅ Files created.")


def setup_venv(base_dir):
    """Creates a virtual environment and installs dependencies inside it."""
    print("🔧 Setting up virtual environment...")
    venv_path = os.path.join(base_dir, ".venv")
    vscode_settings_path = os.path.join(base_dir, ".vscode", "settings.json")

    # Step 1: Create the virtual environment
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    # Step 2: Determine Python executable and pip in the virtual environment
    if os.name == "nt":  # Windows
        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_path, "Scripts", "pip.exe")
    else:  # macOS/Linux
        python_executable = os.path.join(venv_path, "bin", "python")
        pip_executable = os.path.join(venv_path, "bin", "pip")

    # Debugging: Print the paths to the Python and pip executables
    print(f"Using Python from: {python_executable}")
    print(f"Using pip from: {pip_executable}")

    # Check if python and pip exist in the virtual environment
    if not os.path.exists(pip_executable):
        print("❌ pip not found in the virtual environment. Please check the environment.")
        return
    if not os.path.exists(python_executable):
        print("❌ Python not found in the virtual environment. Please check the environment.")
        return

    # Step 3: Install dependencies using pip inside the virtual environment
    subprocess.run([pip_executable, "install", "-r", os.path.join(base_dir, "requirements.txt")], check=True)

    # Step 4: Ensure the .vscode/settings.json directory exists
    if not os.path.exists(os.path.dirname(vscode_settings_path)):
        os.makedirs(os.path.dirname(vscode_settings_path))

    # Step 5: Define the pythonPath for VSCode settings.json
    python_path = (
        os.path.join(venv_path, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(venv_path, "bin", "python")
    )

    vscode_settings = {
        "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
    }

    # Step 6: Write the VSCode settings to the settings.json file
    with open(vscode_settings_path, "w") as settings_file:
        json.dump(vscode_settings, settings_file, indent=4)

    print("✅ Virtual environment created and dependencies installed.")


def cleanup_default_structure(base_dir):
    os.rmdir(f"{base_dir}/config")
    print("✅ Cleaned up default Django structure.")


def create_django_project(base_dir):
    """Creates a Django project inside the given directory without the default settings.py."""
    print("🚀 Creating Django project...")

    venv_python = os.path.join(base_dir, ".venv", "Scripts" if os.name == "nt" else "bin", "python")

    # Create the Django project named "config"
    subprocess.run([venv_python, "-m", "django", "startproject", "config", base_dir], check=True)

    # Remove the default settings.py file
    settings_path = os.path.join(base_dir, "config", "settings.py")
    if os.path.exists(settings_path):
        os.remove(settings_path)

    print("✅ Django project created (without default settings.py).")


def modify_manage_py(base_dir):
    manage_py_path = os.path.join(base_dir, "manage.py")

    with open(manage_py_path, "r") as f:
        content = f.read()

    environment = os.getenv("ENVIRONMENT", "dev")
    settings_module = f"config.settings.{environment}"

    content = content.replace(
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')",
        f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{settings_module}')",  # Dynamically set the environment
    )

    with open(manage_py_path, "w") as f:
        f.write(content)

    print("✅ manage.py modified.")


def modify_wsgi_asgi(base_dir):
    wsgi_path = os.path.join(base_dir, "config", "wsgi.py")
    asgi_path = os.path.join(base_dir, "config", "asgi.py")

    environment = os.getenv("ENVIRONMENT", "dev")  # Get environment dynamically
    settings_module = f"config.settings.{environment}"  # Dynamically set the settings module

    # Modify wsgi.py
    with open(wsgi_path, "r") as f:
        content = f.read()
    content = content.replace(
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')",
        f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{settings_module}')",  # Use dynamic settings
    )
    with open(wsgi_path, "w") as f:
        f.write(content)

    # Modify asgi.py
    with open(asgi_path, "r") as f:
        content = f.read()
    content = content.replace(
        "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')",
        f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{settings_module}')",  # Use dynamic settings
    )
    with open(asgi_path, "w") as f:
        f.write(content)

    print("✅ wsgi.py and asgi.py modified.")


def setup_scripts_folder(project_dir):
    """Ensure the scripts directory exisits and adds the create_app.py script."""

    scripts_dir = os.path.join(project_dir, "scripts")

    # Create scripts directory if it doesn't exist
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    # Define source and destination for create_app.py
    template_app_script = os.path.join(os.path.dirname(__file__), "create_app.py")
    dest_app_script = os.path.join(scripts_dir, "create_app.py")

    # Copy create_app.py if it doesn't already exist in the scripts folder
    if not os.path.exists(dest_app_script):
        shutil.copy(template_app_script, dest_app_script)
        print("✅ `create_app.py` has been added to the `scripts/` folder.")
    else:
        print("ℹ️ `create_app.py` already exists in `scripts/`.")


def main():
    parser = argparse.ArgumentParser(description="Create a Django project with a double-folder structure.")
    parser.add_argument("project_name", type=str, help="The name of the Django project.")
    args = parser.parse_args()

    base_dir = os.path.join(os.getcwd(), args.project_name)
    secret_key = generate_secret_key()

    # Step 1: Create folders and files after setting up the venv
    print(f"🚀 Creating Django project: {args.project_name}")
    create_folders(base_dir)
    create_files(base_dir, secret_key)
    # Step 2: Setup virtual environment first
    setup_venv(base_dir)

    create_django_project(base_dir)

    # Step 2: Modify manage.py to use custom settings
    modify_manage_py(base_dir)

    # Step 3: Modify wsgi.py and asgi.py for environment-specific settings
    modify_wsgi_asgi(base_dir)

    setup_scripts_folder(base_dir)

    print("🎉 Django project setup complete! Activate the virtual environment using:")
    if os.name == "nt":
        print(f"   {base_dir}\\venv\\Scripts\\activate")
    else:
        print(f"   source {base_dir}/.venv/bin/activate")

    print("Then, run:")
    print("   python manage.py runserver")


if __name__ == "__main__":
    main()
