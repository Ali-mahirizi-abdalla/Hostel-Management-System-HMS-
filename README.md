# Hostel Management System (HMS)

A professional web-based Hostel Management System built with Django and Tailwind CSS. This system allows students to manage their meal preferences and provides kitchen staff with real-time data for meal planning.

## Features

### For Students
-   **Dashboard**: View and manage meal preferences for Today and Tomorrow.
-   **Meal Selection**: Toggle Breakfast, Early Breakfast, and Supper.
    -   *Note: Breakfast selection is locked after 8:00 AM for the current day.*
-   **Profile**: Manage contact details and profile picture.
-   **Mobile Reponsive**: Access from any device.

### For Kitchen/Admin
-   **Kitchen Dashboard**: Real-time aggregated counts for meals.
-   **Planning**: Preview meal counts for tomorrow.
-   **Data Export**: Download daily meal reports as CSV.

## Tech Stack
-   **Backend**: Django 4.x
-   **Frontend**: HTML5, Django Templates, Tailwind CSS (CDN)
-   **Database**: SQLite (Dev) / PostgreSQL (Prod)
-   **Deployment**: Ready for PythonAnywhere, Railway, or Render.

## Quick Start

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd Hostel_System
    ```

2.  **Set up Environment**
    ```bash
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Configure**
    Copy `.env.example` to `.env` and adjust settings (optional for local dev).

4.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Start Server**
    ```bash
    python manage.py runserver
    ```
    Visit `http://127.0.0.1:8000/`

## deployment
See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.
