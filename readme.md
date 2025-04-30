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

### Setup and Configuration

Follow the steps below to set up both the backend and frontend components.


#### Clone the repository

```bash
git clone https://github.com/Al-Islaah-khed/KokanIslamicLibrary
```

#### 1. Backend Setup

```bash
cd server
```

##### Setting up the Virtual Environment (Recommended)

It's good practice to use a virtual environment to isolate project dependencies.

```bash
python -m venv venv
```

##### Activating the Virtual Environment

* **On Windows:**
    ```bash
    venv/Scripts/activate
    ```
* **On macOS and Linux:**
    ```bash
    source venv/bin/activate
    ```

##### Installing Backend Dependencies

```bash
pip install -r requirements.txt
```

This command will install all the necessary Python packages listed in the `requirements.txt` file.

##### Configure Environment Variables

create a `.env` file in the `server` directory. This file contains important configuration settings for the backend application.

**It's essential to customize these values according to your specific setup.**

Open the `.env` file and modify the following variables:

* `DATABASE_URL`: This specifies the connection string for your PostgreSQL database.
    * `postgresql://<username>:<password>@<host>:<port>/<database_name>`
    * **Replace:**
        * `<username>` with your PostgreSQL username (you likely set this during installation).
        * `<password>` with your PostgreSQL password.
        * `<host>` with the address of your PostgreSQL server (usually `localhost` if it's running on your local machine).
        * `<port>` with the port your PostgreSQL server is listening on (the default is `5432`).
        * `<database_name>` with the name of the database you want to use for the library management system (e.g., `kokan_library`). You might need to create this database in PostgreSQL if it doesn't exist yet.

* `SECRET_KEY`: This is a secret key used for signing JSON Web Tokens (JWT) for authentication. **It's crucial to keep this key secure and generate a strong, unique value for production environments.** The provided value is a placeholder; consider using a more robust method to generate a secure key.

* `JWT_ALGORITHM`: This specifies the algorithm used for signing JWTs. `HS256` is a common and secure choice. You likely won't need to change this unless you have specific security requirements.

* `ACCESS_TOKEN_EXPIRE_MINUTES`: This determines how long (in minutes) an access token will be valid before it expires. You can adjust this value based on your application's security and usability needs.

**Example `.env` file with customized values:**

```
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/library_db
SECRET_KEY=aVeryLongAndSecureRandomString1234567890abcdef
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Important:** After modifying the `.env` file, ensure you save the changes. The backend application will typically load these environment variables when it starts.

#### 2. Frontend Setup

```bash
cd ../client
```

##### Installing Frontend Dependencies

```bash
npm install
```

This command will download and install all the required JavaScript packages defined in the `package.json` file.

## Running the Application

Once you have completed the setup, you can start the backend and frontend servers.

#### 1. Running the Backend

```bash
cd ../server
venv/Scripts/activate
cd app
fastapi dev main.py
```

This command will start the FastAPI development server. You should see output indicating the server is running, usually on `http://127.0.0.1:8000`.

#### 2. Running the Frontend

Open a new terminal window and navigate to the `client` directory:

```bash
cd ../client
npm run dev
```

This command will start the frontend development server. Typically, this will open your application in a web browser at a specific address (e.g., `http://localhost:5173`). Check the terminal output for the exact address.

That's it! You should now have the Kokan Islamic Library software running on your local machine.
