# Expense Sharing

## Overview

This is an Expense Sharing application built using Django and Django REST framework. The application allows users to add expenses and split them among different participants using various methods (equally, exact amounts, and percentages). Additionally, it includes features to send notifications to participants when a new expense is added and to send weekly summaries of amounts owed.
Also application allow users to get their balance in simplified version.

## Project Structure

- The `expense_sharing/` directory serves as the root directory of the Django project.

    - **`manage.py`**: A command-line utility for managing the project.

    - **`expense_sharing/`**: The main Django app for the Expense Sharing project.

        - **`__init__.py`**: Marks the directory as a Python package.
        
        - **`settings.py`**: Contains project settings and configurations.
        
        - **`urls.py`**: Defines URL patterns for routing requests to views.
        
        - **`wsgi.py`**: Entry point for WSGI-compatible web servers.

    - **`expenses/`**: A secondary app within the project, possibly handling expense-related functionalities.

        - **`migrations/`**: Contains database migration files.
        
        - **`__init__.py`**, **`admin.py`**, **`apps.py`**, **`models.py`**, **`serializers.py`**, **`tests.py`**, **`views.py`**: Standard Django files for defining models, views, serializers, tests, etc.

This structure organizes the project's files and directories according to Django conventions, facilitating easy management and navigation.


## Getting Started

To set up and run the Django project with Django REST Framework:

1. Install Django and Django REST Framework:

    ```bash
    pip install django djangorestframework
    ```

2. Navigate to the project directory:

    ```bash
    cd expense_sharing/
    ```

3. Apply database migrations:

    ```bash
    python3 manage.py migrate
    ```

4. Start the development server:

    ```bash
    python3 manage.py runserver
    ```

5. Access the application at [http://localhost:8000/](http://localhost:8000/).

6. (Optional) Create a superuser to access the Django admin panel:

    ```bash
    python3 manage.py createsuperuser
    ```

    Follow the prompts to create a username, email, and password.

Now you're ready to use the Expense Sharing Django application with Django REST Framework!

## Class Diagram

```bash
+------------+           +------------+        +---------------+       +-----------+
|   User     |           |  Expense   |        |    Balance    |       |ExactAmount|
+------------+           +------------+        +---------------+       +-----------+
| - user_id  |<--------->| - expense_id|<>----<| - user_from   |       | - amount  |
| - name     |           | - paid_by   |        | - user_to     |       | - expense |
| - email    |           | - amount    |        | - amount      |       | - user    |
| - mobile   |           | - expense_type|      +---------------+       +-----------+
|            |           | - date_created |
|            |           | - exact_amounts|
|            |           | - percentages  |
+------------+           +--------------+
    |                           |
    |                           |
    |                           |
+-----------------------------------------------+
|                 |                             |
|   +-------------+             +-------------+  |
|   |participants|             |balances_due |  |
|   +-------------+             +-------------+  |
|                 |                             |
|   +-------------+             +-------------+  |
|   |expenses_paid|             |balances_owed|  |
|   +-------------+             +-------------+  |
|                 |                             |
+------------------------------------------------+
    |                          |
    |                          |
    v                          v
+-----------------------------------------------+
|                  |                          |
|  +---------------+         +----------------+|
|  |Expense         |         |PercentageShare||
|  +---------------+         +----------------+|
|  | - amount       |         | - percentage   ||
|  | - expense_type ||        | - participant  ||
|  | - date_created |         | - expense      ||
|  | - exact_amounts|         +----------------+
|  | - percentages  |
+------------------+

```

# Expense Sharing API Documentation

### 1. Add User

- **Endpoint:** `/api/users`  
- **Method:** POST  
- **Description:** Add a new user to the system.  
- **Request Format:**
    ```json
    {
    "name": "Karan",
    "email": "karanpamnani@gmail.com",
    "mobile": "123456789"
    }
    ```
- **Response Format:**
    ```json
    {
        "user_id": 1,
        "name": "Karan",
        "email": "karanpamnani@gmail.com",
        "mobile": "123456789"
    }
    ```

### 2. Add Expense

**Equal Split**
- **Endpoint:** `/api/expenses`
- **Method:** POST
- **Description:** Adds a new expense along with expense-related details.
- **Request Format:**
    ```json
    {
    "paid_by": 1, 
    "amount": 1000,
    "expense_type": "EQUAL",
    "participants": [1, 2, 3, 4]
    }   
    ```
- **Response Format:**
    ```json
    {
    "expense_id": 1,
    "paid_by": 1, 
    "amount": 1000,
    "expense_type": "EQUAL",
    "participants": [1, 2, 3, 4]
    } 
    ```

**Exact Split**
- **Endpoint:** `/api/expenses`
- **Method:** POST
- **Description:** Adds a new expense along with expense-related details.
- **Request Format:**
    ```json
    {
    "paid_by": 1,
    "amount": 1250,
    "expense_type": "EXACT",
    "participants": [1, 2, 3],
    "exact_amounts": {
        "2": 370,
        "3": 880
    }
    }
    ```
- **Response Format:**
    ```json
    {
    "expense_id": 2,
    "paid_by": 1,
    "amount": 1250,
    "expense_type": "EXACT",
    "participants": [1, 2, 3],
    "exact_amounts": {
        "2": 370,
        "3": 880
    }
    }
    ```

**Percent Split**
- **Endpoint:** `/api/expenses`
- **Method:** POST
- **Description:** Adds a new expense along with expense-related details.
- **Request Format:**
    ```json
    {
    "paid_by": 4,
    "amount": 1200,
    "expense_type": "PERCENT",
    "participants": [1, 2, 3, 4],
    "percentages": {
        "1": 40,
        "2": 20,
        "3": 20,
        "4": 20
    }
    }
    ```

- **Response Format:**
    ```json
    {
    "expense_id": 3,
    "paid_by": 4,
    "amount": 1200,
    "expense_type": "PERCENT",
    "participants": [1, 2, 3, 4],
    "percentages": {
        "1": 40,
        "2": 20,
        "3": 20,
        "4": 20
    }
    }
    ```

### 3. Get balance for single user

- **Endpoint:** `/api/balances/1`  
- **Method:** GET  
- **Description:** Get Balance for single user based on user ID 
- **Response Format:**
    ```json
    [
    {
        "user_from": 1,
        "user_to": 2,
        "amount": "600.00"
    },
    {
        "user_from": 1,
        "user_to": 4,
        "amount": "400.00"
    }
    ]
    ```


### 4. Get Simplified balance

- **Endpoint:** `/api/simplified-balances`  
- **Method:** GET  
- **Description:** Get Simplified Balance
- **Response Format:**
    ```json
    [
    {
        "user_from": "karan",
        "user_to": "mayank",
        "amount": 100.0
    },
    {
        "user_from": "kuldeep",
        "user_to": "mayank",
        "amount": 1000.0
    }
    ]
    ```

### Tasks
- `send_expense_email(expense_id)`
- `send_weekly_summary()`

