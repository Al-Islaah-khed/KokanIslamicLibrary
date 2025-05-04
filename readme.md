# Kokan Islamic Library

This is the software for the Kokan Islamic Library, designed to help with uploading, managing, and organizing books.

## Getting Started

This guide will walk you through the installation and setup process.

### Prerequisites

Before you begin, please ensure you have the following software installed on your system:

1.  **Node.js:** Version `20.19.0`  
    * You can download it from the official [Node.js website](https://nodejs.org/).

2.  **Python:** Version `3.12.0`  
    * Make sure Python is added to your system's PATH. You can download it from the official [Python website](https://www.python.org/downloads/).

3.  **PostgreSQL:** Version `17`  
    * You can download and install it from the official [PostgreSQL website](https://www.postgresql.org/download/). During installation, remember the username, password, and port you set up.

### Project Structure

The project is organized into the following directories:

```
KokanIslamicLibrary/
├── server/     # Contains the backend code
└── client/     # Contains the frontend code
```

---

### Setup and Configuration

Follow the steps below to set up both the backend and frontend components.

---

#### Clone the repository

```bash
git clone https://github.com/Al-Islaah-khed/KokanIslamicLibrary
```

---

## Backend Setup

```bash
cd server
```

### 1. Set up the virtual environment (Recommended)

```bash
python -m venv venv
```

### 2. Activate the virtual environment

* **On Windows:**
    ```bash
    venv/Scripts/activate
    ```

* **On macOS and Linux:**
    ```bash
    source venv/bin/activate
    ```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---
### 4. Configure environment variables

Create a `.env` file in the `server` directory.
You can copy the template from the provided `.env.example` file:

```bash
cp .env.example .env
```

Then, open the `.env` file and update the values as needed:

```env
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/library_db
SECRET_KEY=aVeryLongAndSecureRandomString1234567890abcdef
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace the placeholder values with your actual database credentials and a secure secret key.

---

### 5. Database Setup

#### 5.1 Create the database

In `psql` or a database GUI:

```sql
CREATE DATABASE library_db;
```

#### 5.2 Run Alembic Migrations

Alembic is already initialized and configured.

Run this to apply existing migrations:

```bash
alembic upgrade head
```

#### 5.3 Insert default roles

After migrations, insert these roles into the `roles` table:

```sql
INSERT INTO roles (name, description) VALUES
('super_admin', 'Full access to all system functionalities'),
('librarian', 'Manages books, users, and issues/returns'),
('auditor', 'Can view logs and reports only'),
('admin_staff', 'Manages user accounts and approvals');
```

---

### 6. Working with Alembic

#### Create new migration after changing models:

```bash
alembic revision --autogenerate -m "Your message here"
```

#### Apply latest migrations:

```bash
alembic upgrade head
```

#### Check current database version:

```bash
alembic current
```

**Note:** Alembic reads the database URL from your `.env` file.

---

### 7. Run the Backend

```bash
cd app
fastapi dev main.py
```

This will start the FastAPI server at `http://127.0.0.1:8000`.

---

## 💻 Frontend Setup

```bash
cd ../client
```

### 1. Install dependencies

```bash
npm install
```

### 2. Run the Frontend

```bash
npm run dev
```

This usually starts the frontend at `http://localhost:5173`.

---

## ✅ Final Notes

- Make sure `.env` is created and set up before running any backend commands.
- Alembic is pre-configured, so there's no need to reinitialize it.
- Logs are rotated and managed inside the backend — check the `logs/` directory.

---
