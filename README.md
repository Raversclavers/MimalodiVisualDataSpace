# Mimalodi Visual Data Space

Mimalodi Visual Data Space is a portfolio-ready Django website for presenting data services, case studies, analytics-focused content, and client inquiry workflows.

The project is intentionally built with plain Django views, templates, SQLite, and WhiteNoise so it stays easy to understand, easy to host, and easy to extend.

## What the project includes

- A polished public-facing marketing site
- Service pages and service detail pages
- Portfolio and case study pages
- A contact workflow backed by Django models and admin
- Blog and tutorial sections
- Admin-managed content for portfolio and services
- Production-minded static file handling with WhiteNoise

## Stack

- Python 3.12
- Django 5.1
- SQLite for the first live version
- Gunicorn for production WSGI serving
- WhiteNoise for static assets

## Local development

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file or set environment variables in your shell.

Minimum values:

```text
DJANGO_SECRET_KEY=replace-with-a-real-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

You can use [.env.example](.env.example) as a reference.

### 4. Run migrations

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

### 6. Create an admin user

```powershell
python manage.py createsuperuser
```

## Common development commands

Run tests:

```powershell
python manage.py test
```

Run deployment checks:

```powershell
python manage.py check --deploy
```

Collect static files:

```powershell
python manage.py collectstatic --noinput
```

## Deployment

This repository is prepared for simple first deployments on platforms like PythonAnywhere and Render.

Deployment assets included in the repo:

- [Procfile](Procfile)
- [build.sh](build.sh)
- [.env.example](.env.example)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md)
- [PRELAUNCH_CHECKLIST.md](PRELAUNCH_CHECKLIST.md)

For the full deployment walkthrough, including PythonAnywhere setup and environment variable examples, see [DEPLOYMENT.md](DEPLOYMENT.md).

For a beginner-friendly PythonAnywhere free-host deployment guide tailored to this repository, see [PYTHONANYWHERE_DEPLOY.md](PYTHONANYWHERE_DEPLOY.md).

For a beginner-friendly launch QA pass before going live, use [PRELAUNCH_CHECKLIST.md](PRELAUNCH_CHECKLIST.md).

## Repository hygiene

This project should not commit local-only or generated artifacts such as:

- virtual environments
- Python bytecode caches
- local SQLite databases
- collected static build output
- uploaded media assets
- local environment files with secrets

The ignore rules are already configured in [.gitignore](.gitignore). If those paths were committed earlier, they must also be removed from git tracking once.

Recommended cleanup commands:

```powershell
git rm -r --cached venv staticfiles media
git rm -r --cached core/__pycache__ mimalodivisualdataspace/__pycache__
git rm --cached db.sqlite3
```

Then commit the cleanup:

```powershell
git commit -m "Remove tracked generated files"
```

These commands remove files from version control only. They do not delete your local working copies.

## Portfolio positioning

This codebase is structured to present:

- a professional analytics and reporting brand
- portfolio-backed services
- production-minded Django fundamentals
- a clear path from local development to low-cost deployment

That makes it suitable both as a real business site and as a portfolio project demonstrating practical Django engineering.
