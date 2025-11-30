# Smart Task Analyzer

A Django-based task prioritization tool that calculates a "Priority Score" for tasks based on Urgency (Due Date), Importance, and Effort. This project uses `uv` for modern, fast Python package management.

---

## 🚀 Prerequisites

- **Python** (3.12+)
- **uv** (An extremely fast Python package installer and resolver)
  - *To install uv:* `pip install uv`

---

## 🛠 Step 1: Project Initialization & Environment

We use `uv` instead of standard pip/venv because it is faster and manages dependencies via a `pyproject.toml` file.

### 1.1 Create the project folder and initialize
bash
uv init task-analyzer
cd task-analyzer
`

  * `uv init`: Creates a project folder with a `pyproject.toml` file (modern standard for Python configuration).

### 1.2 Install Django & CORS Headers

bash
uv add django
uv add django-cors-headers


  * `uv add`: Replaces `pip install`. It downloads Django and locks the specific version in a `uv.lock` file so your project never breaks due to unexpected updates.
  * It automatically creates a `.venv` folder containing all libraries.

-----

## ⚙ Step 2: Backend Setup (Django)

### 2.1 Create the Django Project Structure

bash
uv run django-admin startproject backend .


  * This creates the `backend` folder and the important `manage.py` file in the current directory.

### 2.2 Create the 'tasks' App

bash
uv run python manage.py startapp tasks


  * This creates the `tasks` folder where our logic (`models.py`, `views.py`) lives.

### 2.3 Connect the App & Enable CORS

We need to connect the new app and enable CORS so the frontend can talk to the backend.

**Open `backend/settings.py` and update:**

1.  **Find `INSTALLED_APPS` and add:**

    python
    INSTALLED_APPS = [
        # ... default apps ...
        'tasks',                 # <--- Add your app
        'corsheaders',           # <--- Add CORS library
    ]
    

2.  **Find `MIDDLEWARE` and add (Must be at the top\!):**

    python
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',  # <--- Must be first!
        'django.middleware.common.CommonMiddleware',
        # ... other middleware ...
    ]
    

3.  **Add CORS Permission (Anywhere in settings.py):**

    python
    CORS_ALLOW_ALL_ORIGINS = True
    

-----

## 🗄 Step 3: Database Setup (SQLite)

Django comes with SQLite built-in (it is a file, not a server).

### 3.1 Create Migration Scripts

(This tells Django you created/changed a `Task` model in `models.py`)

bash
uv run python manage.py makemigrations


### 3.2 Apply Migrations

(This actually creates the tables in `db.sqlite3`)

bash
uv run python manage.py migrate


-----

## 🖥 Step 4: Running the Application (CRITICAL)

To run this full stack application properly and avoid browser reload issues, you need **two separate terminals**.

### Terminal 1: The Backend (Django)

Starts the API server on port 8000.

bash
uv run python manage.py runserver


  * **API Address:** `http://127.0.0.1:8000/`

### Terminal 2: The Frontend (Python HTTP Server)

We use a separate Python server for the frontend to avoid conflicts with VS Code Live Server (which forces reloads when the database changes).

1.  **Navigate to the project root** (where `manage.py` is).
2.  **Run the frontend on Port 8080:**
    bash
    uv run python -m http.server 8080 --directory frontend
    
3.  **Open in Browser:** Go to **[http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)**

-----

## 🧪 Step 5: Testing the Algorithm

We have created a custom algorithm to calculate task scores. To ensure the math works (e.g., overdue tasks get higher scores), run the unit tests.

bash
uv run python manage.py test tasks


*This runs the test cases defined in `tasks/tests.py`.*

-----

## 📂 Project Structure

text
task-analyzer/
├── .venv/                 # Virtual environment (managed by uv)
├── backend/               # Django project settings (settings.py, urls.py)
├── frontend/              # Frontend code
│   ├── index.html
│   └── script.js
├── tasks/                 # The main app
│   ├── migrations/        # DB migration files
│   ├── models.py          # Database schema (Task class)
│   ├── views.py           # API Logic & Scoring Algorithm
│   ├── tests.py           # Unit tests
│   └── urls.py            # API routes
├── db.sqlite3             # SQLite Database file
├── manage.py              # Django command-line utility
├── pyproject.toml         # Dependency configuration
└── uv.lock                # Locked versions of dependencies
```