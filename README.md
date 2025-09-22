# SpaceX Launch Tracker

## Introduction

SpaceX Launch Tracker is a Python-based web application built using Django and Django REST Framework (DRF) to track and analyze SpaceX launches. It fetches data from the SpaceX public API v4, stores it in a local database for efficient querying, and provides RESTful endpoints for viewing launches with filtering capabilities and generating statistics. The project emphasizes performance through caching syncing the data fetched from SpaceX API.

### Key Features
- **Data Fetching**: Retrieves launches, rockets, and launchpads from the SpaceX API and stores them in a database.
- **Launch Listing**: Provides a REST API to list launches with filters for date range, rocket name, success status, and launch site.
- **Statistics**: Generates insights like success rates by rocket, total launches per site, and launch frequency (monthly/yearly).
- **Caching**: Uses `LocMemCache` to cache API responses for faster access. Cache is set for 86400s (a day).
- **Sync SpaceX**: Supports data sync via a custom Django management command.
- **Testing**: Includes tests in `tests/` using `pytest-django` and `pytest-mock` to verify API functionality and caching.
- **Browse-able APIs**: Minimal API interface to showcase the APIs response. See **API Endpoints** section below for details.

The project uses Poetry for dependency management, with the Django project in `src/` and tests in a separate `tests/` directory.

## Prerequisites

Ensure the following are installed before setting up the project:

1. **Python 3.11+**:
   - Download from [python.org](https://www.python.org/downloads/).
   - Set `PATH` environment variable
   - Verify: `python --version`.

2. **Poetry 2.2.0+**:
   - Install: `pip install poetry==2.2.0`.
   - Set `PATH` environment variable
   - Verify: `poetry --version`.

3. **Caching**:
   - For the sake of simplicity `LocMemCache` is used.
   - For persistent caching cache like Memcache can be used.

4. **Database**:
   - SQLite is used by default (no installation needed).

## Setup Instructions

Follow these steps to set up the project locally. Use Windows Command Prompt (cmd) for all commands.

1. **Clone the Repository**:
   ```cmd
   git clone <repository-url>
   cd spacex-launch-tracker
   ```
   Replace `<repository-url>` with repository URL.

2. **Install Dependencies**:
   Install all dependencies using Poetry by running below command in root directory:
   ```cmd
   poetry install
   ```
   - This creates a virtual environment in virtualenvs folder of pypoetry. Copy the complete path.

3. **Activate the Virtual Environment**:<br>
   For Windows:
   ```cmd
   <copied path from last point>\Scripts\activate
   ```
   For mac/linux:<br>
   ```cmd
   source <copied path from last point>\bin\activate
   ```
   - This activates the virtual environment. Run all subsequent commands inside this shell.

4. **Run Database Migrations**:
   Navigate to `src/` (where `manage.py` is):
   ```cmd
   cd src
   python manage.py migrate
   ```
   - This applies migrations for models (`Rocket`, `Launchpad`, `Launch`) to the SQLite database (`db.sqlite3`).

5. **Fetch Initial Data**:
   Populate the database with SpaceX API data:
   - Navigate to `src/` (where `manage.py` is)
   ```cmd
   python manage.py fetch_spacex_data
   ```
   - This runs the `fetch_spacex_data` management command to fetch rockets, launchpads, and launches from SpaceX API.

## Running the Project

Before running project, data must be fetched from SpaceX API by running below command in `src/` directory:

   ```cmd
   python manage.py fetch_spacex_data
   ```

The command is following sync pattern. It will always create non-existing objects in the database.

### Start the Development Server: <br>

From `src/`:
```cmd
python manage.py runserver
```

- **BASE_URL** = `http://127.0.0.1:8000/`.
- Press `Ctrl+C` to stop.


## API Endpoints

The SpaceX Launch Tracker provides RESTfull API endpoints to retrieve launch data and statistics. All endpoints are prefixed with `/api/v1/`. Responses are in JSON format, paginated by 100 items per page.

> Note: APIs have an interface. Any browser can be used to explore them.

| Endpoint                      | Method | Description                                      | Query Parameters                                                                      |
|-------------------------------|--------|--------------------------------------------------|---------------------------------------------------------------------------------------|
| `{BASE_URL}/api/v1/launches/` | GET    | List all launches with optional filtering        | `launch_datetime__gte`, `launch_datetime__lte`, `rocket__name`, `success`, `launchpad__name` |
| `{BASE_URL}/api/v1/launches/<id>/`      | GET    | Retrieve details of a specific launch by ID      | None                                                                                  |
| `{BASE_URL}/api/v1/stats/`              | GET    | Retrieve launch statistics (success rates, etc.) | None                                                                                  |

### Query Parameter Details
- **launch_datetime__gte**: Filter launches on or after a date (e.g., `2020-01-01T00:00:00Z`).
- **launch_datetime__lte**: Filter launches on or before a date (e.g., `2020-12-31T23:59:59Z`).
- **rocket__name**: Filter by rocket name (exact match, e.g., `Falcon 9`).
- **success**: Filter by success status (e.g., `true` or `false`).
- **launchpad__name**: Filter by launchpad name (exact match, e.g., `VAFB SLC 4E`).

### Notes
- **Pagination**: Use `?page=<number>` to navigate pages (e.g., `/api/v1/launches/?page=2`).
- **Caching**: Responses are cached for 86400 seconds (configurable in ViewSets individually).
- **Authentication**: None

## Running Tests

Tests are located in `tests/` and use `pytest-django` for Django-specific testing.

1. **Ensure Dependencies**:
   ```cmd
   poetry install
   ```

2. **Run All Tests**:<br>
   First create and activate virtual environment as explained above then from the project root:
   ```cmd
   pytest
   ```
   - This discovers all tests in `tests/` matching `test_*.py` or `*tests.py`.
