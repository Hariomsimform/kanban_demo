# KanBan Demo Project

This is simple project management system

## Prerequisites

Make sure you have the following installed on your machine:

- Python3.8
- pip (Python package installer)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Hariomsimform/kanban_demo.git
    cd kanban_project
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    ```bash
    source venv/bin/activate  # For Linux/Mac
    # or
    venv\Scripts\activate  # For Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

## Run the Development Server

```bash
python manage.py runserver
