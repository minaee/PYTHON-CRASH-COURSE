# Personal Finance & Learning Log

> A full-stack web application built with Django and React — deployed on a Linux server.

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.x-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

🌐 **Live Demo:** [http://minaee.duckdns.org](http://minaee.duckdns.org)

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [License](#license)

---

## About

A full-stack web app with two modules: a **Learning Log** for journaling topics and entries, and a **Finance Tracker** for managing personal income and expenses with interactive charts. Built initially from the *Python Crash Course* book by Eric Matthes, then significantly extended with a REST API layer and a React frontend.

---

## ✨ Features

### Learning Log
- ✅ Create and manage learning topics
- ✅ Add and edit journal entries per topic
- ✅ All data is private — each user only sees their own topics

### Finance Tracker
- ✅ Add income and expense transactions
- ✅ Interactive pie chart — spending breakdown by category
- ✅ Bar chart — monthly income vs expenses
- ✅ Summary dashboard — total income, total expenses, net balance
- ✅ Real-time UI updates without page reloads (React)

### General
- ✅ User registration, login, and logout
- ✅ Fully deployed on a Linux server (Gunicorn + Nginx)

---

## 🛠 Tech Stack

| Layer         | Technology                        |
|---------------|-----------------------------------|
| Backend       | Django 6, Python 3.14             |
| Database      | PostgreSQL                        |
| Frontend      | React 19, Recharts, Bootstrap 5   |
| Build Tool    | Vite 8                            |
| Auth          | Django built-in auth              |
| Deployment    | Gunicorn, Nginx, DuckDNS          |

---

## 🏗 Architecture

This project uses a **Django + React islands** architecture:

- Django handles routing, authentication, database access, and server-rendered templates
- React is embedded as an interactive island inside the Finance page
- The React component communicates with Django via a JSON REST API
- Vite compiles the React code into static assets, served by Django's static file pipeline

```
Browser
  ├── Django templates (Learning Log, Auth pages)
  └── React island (Finance dashboard)
        └── fetches from Django JSON API
              └── PostgreSQL
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- Node.js 18+
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/minaee/PYTHON-CRASH-COURSE.git
   cd PYTHON-CRASH-COURSE
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values (see below)
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Build the React frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   python manage.py collectstatic
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   Visit [http://localhost:8000](http://localhost:8000) 🎉

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_NAME=ll_project_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

---

## 📡 API Reference

All endpoints require authentication (session-based).

| Method | Endpoint                        | Description                        |
|--------|---------------------------------|------------------------------------|
| GET    | `/finance/api/transactions/`    | List all transactions for the user |
| POST   | `/finance/api/transactions/add/`| Create a new transaction           |
| GET    | `/finance/api/summary/`         | Get totals, chart data, and net balance |

### Example — GET `/finance/api/transactions/`

```json
[
  {
    "date": "2025-04-01",
    "amount": "50.00",
    "category": "Groceries",
    "description": "Weekly shop",
    "type": "expense"
  }
]
```

### Example — POST `/finance/api/transactions/add/`

```json
{
  "date": "2025-04-01",
  "amount": "50.00",
  "category": "Groceries",
  "description": "Weekly shop",
  "type": "expense"
}
```

### Example — GET `/finance/api/summary/`

```json
{
  "total_income": 3000.00,
  "total_expenses": 1250.00,
  "net": 1750.00,
  "by_category": [
    { "category": "Groceries", "total": "300.00" }
  ],
  "monthly": [
    { "month": "2025-04", "income": 3000.00, "expense": 1250.00 }
  ]
}
```

---

## 📁 Project Structure

```
PYTHON-CRASH-COURSE/
├── accounts/               # User registration & auth
├── finance/                # Finance tracker app
│   ├── models.py           # Transaction model
│   ├── views.py            # Template views + JSON API views
│   └── urls.py
├── frontend/               # React frontend (Vite)
│   ├── src/
│   │   ├── main.jsx        # React entry point
│   │   └── TransactionsApp.jsx  # Main React component
│   └── vite.config.js
├── learning_logs/          # Learning log app
├── ll_project/             # Django project settings
├── static/                 # Source static files
├── staticfiles/            # Compiled static files (collectstatic output)
├── templates/              # Django HTML templates
├── requirements.txt
└── manage.py
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Python Crash Course](https://nostarch.com/python-crash-course) by Eric Matthes — the starting point for this project
- [Django](https://www.djangoproject.com/)
- [React](https://react.dev/)
- [Recharts](https://recharts.org/)