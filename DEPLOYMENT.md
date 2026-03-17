# Deployment Guide

This project is prepared for a simple first live deployment using:

- Django
- SQLite
- Gunicorn
- WhiteNoise for static files

It is set up to work well for:

- Render
- PythonAnywhere

For the first live version, SQLite is intentionally kept to reduce setup complexity.

## 1. Required Environment Variables

Set these values on your hosting platform:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`

Recommended:

- `DJANGO_CSRF_TRUSTED_ORIGINS`

Optional:

- `DEFAULT_FROM_EMAIL`
- `CONTACT_NOTIFICATION_EMAIL`
- `SQLITE_PATH`

Use [.env.example](.env.example) as your reference.

## 2. What This Project Already Handles

- Static files are served with WhiteNoise.
- `collectstatic` is handled by `build.sh`.
- `migrate` runs automatically on startup from the `Procfile`.
- `DEBUG` and `ALLOWED_HOSTS` are environment-driven.
- SQLite remains the default database for the first deployment.

## 3. Deploying to Render

### Create the service

1. Push this project to GitHub.
2. In Render, create a new `Web Service` from that repository.
3. Select the Python environment.

### Recommended Render settings

- Build Command:

```bash
./build.sh
```

- Start Command:

```bash
gunicorn mimalodivisualdataspace.wsgi --log-file -
```

If Render is configured to read the `Procfile`, that is also fine.

### Environment variables for Render

Set:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=your-app.onrender.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`

Optional:

- `RENDER_EXTERNAL_HOSTNAME` is usually provided automatically by Render.

### Important SQLite note for Render

Render free instances use ephemeral storage. That means your SQLite database can be reset on redeploy or restart.

This is acceptable for a first live demo, but not for important long-term data.

If you later move beyond a demo launch, switch to Postgres.

## 4. Deploying to PythonAnywhere

For a full beginner-friendly step-by-step guide tailored to this exact repository, including GitHub push, Bash console commands, WSGI edits, static/media mapping, and common error troubleshooting, see [PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md).

### Upload the project

1. Upload the project files or clone the repository on PythonAnywhere.
2. Open a Bash console.
3. Create or activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure environment values

Set the needed environment variables in your PythonAnywhere WSGI file or your startup configuration.

At minimum set:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com`

One simple PythonAnywhere approach is to add them near the top of your WSGI file before `get_wsgi_application()` is called:

```python
import os

os.environ['DJANGO_SECRET_KEY'] = 'replace-with-your-real-secret-key'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://yourusername.pythonanywhere.com'
```

If you want contact form emails enabled on first launch, also set:

```python
os.environ['DEFAULT_FROM_EMAIL'] = 'you@example.com'
os.environ['CONTACT_NOTIFICATION_EMAIL'] = 'you@example.com'
```

### Run setup commands

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### WSGI configuration

Point your PythonAnywhere web app to:

```python
application = get_wsgi_application()
```

using [mimalodivisualdataspace/wsgi.py](mimalodivisualdataspace/wsgi.py).

### PythonAnywhere launch order

1. Create the web app and point it at your project directory.
2. Install dependencies with `pip install -r requirements.txt` inside the PythonAnywhere virtualenv.
3. Add the environment variables in the WSGI file.
4. Run `python manage.py migrate`.
5. Run `python manage.py collectstatic --noinput`.
6. Reload the web app from the PythonAnywhere dashboard.

## 5. Local Production-Style Check

Before deploying, you can test production settings locally:

### PowerShell

```powershell
$env:DJANGO_DEBUG='False'
$env:DJANGO_SECRET_KEY='replace-me-with-a-real-secret-key'
$env:DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'
$env:DJANGO_CSRF_TRUSTED_ORIGINS='http://localhost:8000'
python manage.py check --deploy
```

## 6. First Launch Checklist

1. Set your environment variables.
2. Install dependencies.
3. Run migrations.
4. Run `collectstatic`.
5. Confirm the home page, contact form, portfolio, and admin all load.
6. Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## 7. Recommended Next Upgrade

For a very first live version, SQLite is fine if the site is mostly brochure-style content.

When you are ready for stronger persistence and safer production hosting, the next upgrade should be moving from SQLite to Postgres.

## 8. Repo Cleanup After First Launch

The project already ignores generated folders in [.gitignore](.gitignore), but some generated content was committed earlier and is still tracked by git.

After your first live deployment is stable, clean that out of version control so future `collectstatic` runs stay quieter and the repository stays smaller.

Use these commands from the project root:

```powershell
git rm -r --cached venv staticfiles
git rm -r --cached core/__pycache__ mimalodivisualdataspace/__pycache__
git commit -m "Remove tracked generated files"
```

Optional cleanup if you do not want the local SQLite database committed either:

```powershell
git rm --cached db.sqlite3
git commit -m "Stop tracking local SQLite database"
```

These commands remove the files from git tracking only. They do not delete your local working copies because `--cached` keeps the files on disk.
