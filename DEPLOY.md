# Deployment Instructions

## General Project Setup
1.  Clone the repository.
2.  Set environment variables (see `.env.example`).
    -   `SECRET_KEY`
    -   `DEBUG=False`
    -   `ALLOWED_HOSTS`
    -   `DATABASE_URL` (if using Postgres)
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run migrations: `python manage.py migrate`
5.  Collect static files: `python manage.py collectstatic`

## PythonAnywhere
1.  **Virtualenv**: Create a virtualenv: `mkvirtualenv --python=/usr/bin/python3.10 myenv`
2.  **Code**: Pull your code to `~/Hostel_System`.
3.  **Web Tab**:
    -   Source code directory: `/home/yourusername/Hostel_System`
    -   Virtualenv: `/home/yourusername/.virtualenvs/myenv`
    -   WSGI Config: Add environment variables here using `os.environ` or load from `.env` file.
4.  **Static Files**: Map `/static/` to `/home/yourusername/Hostel_System/staticfiles`.

## Railway / Render
1.  Connect GitHub repo.
2.  **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3.  **Start Command**: `gunicorn Hostel_System.wsgi`
4.  **Variables**: Add `DATABASE_URL`, `SECRET_KEY`, etc. in the dashboard.
