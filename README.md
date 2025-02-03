# Django Project Setup Script 🚀🎯✨

This script automates the creation of a Django project with a double-folder structure hierarchy, environment-based settings, and a virtual environment for dependency management. 🎨🔧📂

## Features ⚡🔥🚀

- Generates a secure `SECRET_KEY` for Django.
- Creates a structured folder hierarchy.
- Initializes a virtual environment and installs dependencies.
- Creates `.env` files for different environments (development, staging, production).
- Modifies `manage.py`, `wsgi.py`, and `asgi.py` to dynamically use the environment settings.
- **Available as a CLI tool with system path configuration!** 🎉🖥️💡

## Installation & Usage 🛠️📌💻

### Windows 🏁🖥️🔄

#### Where to Store the Script 📂📍💾

Save the script and bat file in a permanent location, such as:

```
C:\Users\YourUsername\django-scripts\
```

#### Adding to System Path ⚙️🔗📝

1. Open **System Properties** > **Advanced** > **Environment Variables**.
2. Under **System Variables**, find `Path` and edit it.
3. Add the directory path where the script is stored, e.g., `C:\Users\YourUsername\django-scripts\`.
4. Click **OK** and restart your terminal. ✅🔄🖥️

#### How to Use 🚀💡🎯

1. Open **Command Prompt** or **PowerShell**.
2. Run the CLI command with the project name:

   ```
   create-django myproject
   ```

3. Once completed, activate the virtual environment:

   ```
   myproject\.venv\Scripts\activate
   ```

4. Navigate to the project directory and start the development server:

   ```
   cd myproject
   python manage.py runserver
   ```

### macOS/Linux 🍎🐧💻

**Note: macOS/Linux users need to try and test it out as this has been done in windows**

#### Where to Store the Script 📂📍💾

Store the script in a preferred directory, such as:

```
/home/yourusername/django-scripts/
```

#### Adding to System Path ⚙️🔗📝

1. Open the terminal and edit your shell profile:

   ```
   nano ~/.bashrc  # or ~/.zshrc for macOS users
   ```

2. Add the following line:

   ```
   export PATH="$HOME/django-scripts:$PATH"
   ```

3. Save and exit (`CTRL+X`, then `Y`, then `Enter`).
4. Reload the shell configuration:

   ```
   source ~/.bashrc  # or source ~/.zshrc
   ```

#### How to Use 🚀💡🎯

1. Open **Terminal**.
2. Run the CLI command with the project name:

   ```
   setup_django myproject
   ```

3. Once completed, activate the virtual environment:

   ```
   source myproject/.venv/bin/activate
   ```

4. Navigate to the project directory and start the development server:

   ```
   cd myproject
   python manage.py runserver
   ```

## Environment Configuration 🛠️🔑📜

The script generates a `.env` file inside the `config/` directory with predefined environment variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=dev
DATABASE_URL_DEV=postgres://user:password@localhost:5432/dev_db
DATABASE_URL_STAGING=postgres://user:password@localhost:5432/staging_db
DATABASE_URL_PROD=postgres://user:password@localhost:5432/prod_db
DJANGO_SETTINGS_MODULE=config.settings.dev
```

Modify these variables as needed based on your deployment. 🔄📝⚡

## Notes 📝💡📌

- Make sure you have Python and `pip` installed before running the script.
- Update the `requirements.txt` file to include additional dependencies as needed.
- The script defaults to using PostgreSQL, but you can modify it to use a different database engine if required. 🔄🔧💾

## License 📜⚖️🆓

This project is open-source and can be modified or distributed freely.

---
