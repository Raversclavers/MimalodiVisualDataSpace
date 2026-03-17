# PythonAnywhere Free Deployment Guide

This guide is tailored to this exact Django project:

- project folder: `MimalodiVisualDataSpace`
- Django settings module: `mimalodivisualdataspace.settings`
- WSGI entry point: `mimalodivisualdataspace.wsgi`
- GitHub remote: `https://github.com/Raversclavers/MimalodiVisualDataSpace.git`

Use this when you want your first live deployment on PythonAnywhere free.

## 1. Before you begin

Make sure these files already exist in your repo:

- `requirements.txt`
- `manage.py`
- `mimalodivisualdataspace/wsgi.py`
- `.env.example`

Also make sure your latest changes are committed locally.

## 2. Push the project to GitHub

If your local changes are not pushed yet, run these commands on your own computer from the project root:

```powershell
git status
git add .
git commit -m "Prepare project for PythonAnywhere deployment"
git push origin main
```

If your default branch is not `main`, replace `main` with your actual branch name.

You can confirm the remote is already configured for this repo:

```powershell
git remote -v
```

This project currently points to:

```text
https://github.com/Raversclavers/MimalodiVisualDataSpace.git
```

## 3. Create the PythonAnywhere web app

1. Sign in to PythonAnywhere.
2. Open the `Web` tab.
3. Click `Add a new web app`.
4. Choose your free domain name.
5. When asked for the framework, choose `Manual configuration`.
6. Choose the newest Python version PythonAnywhere offers for free that is compatible with Django 5.1.

If Python 3.12 is available, use it. If not, use the newest supported option shown there.

After the app is created, PythonAnywhere will generate:

- a web app dashboard
- a WSGI configuration file
- a default source-code path

## 4. Open a Bash console and clone the repo

1. Open the `Consoles` tab.
2. Start a new `Bash` console.
3. Run these commands:

```bash
cd ~
git clone https://github.com/Raversclavers/MimalodiVisualDataSpace.git
cd MimalodiVisualDataSpace
```

Pass if:

- the repository clones successfully
- you can see `manage.py` in the project folder

## 5. Create and activate a virtualenv

In the PythonAnywhere Bash console, run:

```bash
cd ~/MimalodiVisualDataSpace
python3.12 -m venv ~/.virtualenvs/mvds-venv
source ~/.virtualenvs/mvds-venv/bin/activate
```

If `python3.12` is not available on your PythonAnywhere account, use the version you selected during web app creation, for example:

```bash
python3.11 -m venv ~/.virtualenvs/mvds-venv
source ~/.virtualenvs/mvds-venv/bin/activate
```

Pass if:

- your shell prompt shows the virtualenv name
- `which python` points inside `~/.virtualenvs/mvds-venv`

## 6. Install requirements

With the virtualenv activated, run:

```bash
cd ~/MimalodiVisualDataSpace
pip install --upgrade pip
pip install -r requirements.txt
```

Pass if:

- Django installs successfully
- WhiteNoise installs successfully
- Pillow installs successfully
- there are no fatal package build errors

## 7. Set environment variables

This project reads settings from environment variables, including:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- optional email variables

For PythonAnywhere, the simplest beginner-friendly approach is to set them directly in the WSGI file.

You will add them before Django loads the app.

Use these real values, replacing `yourusername` with your PythonAnywhere username:

```python
os.environ['DJANGO_SECRET_KEY'] = 'replace-with-a-long-random-secret-key'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://yourusername.pythonanywhere.com'
```

Optional for contact email notifications:

```python
os.environ['DEFAULT_FROM_EMAIL'] = 'you@example.com'
os.environ['CONTACT_NOTIFICATION_EMAIL'] = 'you@example.com'
```

Optional if you want SQLite stored somewhere explicit:

```python
os.environ['SQLITE_PATH'] = '/home/yourusername/MimalodiVisualDataSpace/db.sqlite3'
```

For this project, the default SQLite location is already the project root, so `SQLITE_PATH` is optional.

## 8. Run migrations

Still in the Bash console, with the virtualenv active:

```bash
cd ~/MimalodiVisualDataSpace
python manage.py migrate
```

Pass if:

- migrations complete successfully
- no missing table or import errors appear

Important for this project:

- the service pages depend on the `Service` and `ServiceDeliverable` tables
- make sure all `core` migrations apply, including the service migration

## 9. Collect static files

Run:

```bash
cd ~/MimalodiVisualDataSpace
python manage.py collectstatic --noinput
```

Pass if:

- collectstatic completes successfully
- the `staticfiles` folder is populated on the server

For this project, static settings are already configured in Django:

- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`

## 10. Edit the WSGI file

Go back to the PythonAnywhere `Web` tab.

Open the WSGI file PythonAnywhere created. Its path usually looks like this:

```text
/var/www/yourusername_pythonanywhere_com_wsgi.py
```

Replace the generated contents with this version adapted for this project:

```python
import os
import sys

project_home = '/home/yourusername/MimalodiVisualDataSpace'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SECRET_KEY'] = 'replace-with-a-long-random-secret-key'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://yourusername.pythonanywhere.com'

# Optional email settings
# os.environ['DEFAULT_FROM_EMAIL'] = 'you@example.com'
# os.environ['CONTACT_NOTIFICATION_EMAIL'] = 'you@example.com'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mimalodivisualdataspace.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

Important:

- replace `yourusername` everywhere with your real PythonAnywhere username
- replace the secret key with a real secret value
- keep the settings module exactly as `mimalodivisualdataspace.settings`

## 11. Configure the virtualenv path in the Web tab

In the PythonAnywhere `Web` tab, find the `Virtualenv` field and set it to:

```text
/home/yourusername/.virtualenvs/mvds-venv
```

Save the change.

## 12. Configure static and media paths

In the PythonAnywhere `Web` tab, scroll to the `Static files` section.

Add this mapping:

- URL: `/static/`
- Directory: `/home/yourusername/MimalodiVisualDataSpace/staticfiles`

If you want uploaded images to be served too, add:

- URL: `/media/`
- Directory: `/home/yourusername/MimalodiVisualDataSpace/media`

These paths match this project exactly.

## 13. Create an admin user

In the Bash console, run:

```bash
cd ~/MimalodiVisualDataSpace
source ~/.virtualenvs/mvds-venv/bin/activate
python manage.py createsuperuser
```

Use that account to sign in at:

```text
https://yourusername.pythonanywhere.com/admin/
```

## 14. Reload the app

Go back to the `Web` tab and click `Reload`.

Then open:

```text
https://yourusername.pythonanywhere.com/
```

Check:

- home page loads
- CSS loads
- images load
- `/services/` loads
- one service detail page loads
- `/portfolio/` loads
- `/contact/` loads
- `/admin/` loads

## 15. Troubleshooting common errors

### 400 Bad Request

Usually caused by bad host or CSRF settings.

Check:

- `DJANGO_ALLOWED_HOSTS` contains exactly `yourusername.pythonanywhere.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` contains exactly `https://yourusername.pythonanywhere.com`
- there are no extra quotes inside the domain values

After fixing, reload the web app.

### 403 Forbidden

Common causes:

- CSRF trusted origins missing or wrong
- submitting a POST form over HTTPS with HTTP-only origin configured

Fix:

- make sure the WSGI file sets `DJANGO_CSRF_TRUSTED_ORIGINS` to the full HTTPS URL
- reload the app after editing the WSGI file

### DisallowedHost error

Cause:

- your domain is not listed in `DJANGO_ALLOWED_HOSTS`

Fix:

- set `DJANGO_ALLOWED_HOSTS` to `yourusername.pythonanywhere.com`
- reload the app

### Missing static files or unstyled pages

Cause:

- `collectstatic` was not run
- the `/static/` mapping in PythonAnywhere points to the wrong directory

Fix:

1. Re-run:

```bash
cd ~/MimalodiVisualDataSpace
source ~/.virtualenvs/mvds-venv/bin/activate
python manage.py collectstatic --noinput
```

1. Confirm the Web tab maps `/static/` to:

```text
/home/yourusername/MimalodiVisualDataSpace/staticfiles
```

1. Reload the app.

### Admin works but images do not load

Cause:

- `/media/` is not mapped in the Web tab

Fix:

- add the `/media/` mapping to `/home/yourusername/MimalodiVisualDataSpace/media`
- reload the app

### WSGI import error

Common causes:

- wrong project path in `sys.path`
- wrong settings module name
- virtualenv path not configured in the Web tab

Fix:

- confirm project path is `/home/yourusername/MimalodiVisualDataSpace`
- confirm settings module is `mimalodivisualdataspace.settings`
- confirm virtualenv path is `/home/yourusername/.virtualenvs/mvds-venv`

### ModuleNotFoundError for Django or WhiteNoise

Cause:

- requirements were not installed in the same virtualenv the web app uses

Fix:

```bash
source ~/.virtualenvs/mvds-venv/bin/activate
cd ~/MimalodiVisualDataSpace
pip install -r requirements.txt
```

Then confirm the `Virtualenv` field in the Web tab points to the same environment and reload the app.

## 16. Post-deploy smoke test

After the site loads, test these URLs:

- `https://yourusername.pythonanywhere.com/`
- `https://yourusername.pythonanywhere.com/services/`
- `https://yourusername.pythonanywhere.com/portfolio/`
- `https://yourusername.pythonanywhere.com/contact/`
- `https://yourusername.pythonanywhere.com/admin/`

Also test:

- a valid contact form submission
- admin login
- one service detail page
- one portfolio detail page

## 17. If you update the project later

When you push new code to GitHub, update the PythonAnywhere copy with:

```bash
cd ~/MimalodiVisualDataSpace
git pull
source ~/.virtualenvs/mvds-venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click `Reload` in the PythonAnywhere `Web` tab.
