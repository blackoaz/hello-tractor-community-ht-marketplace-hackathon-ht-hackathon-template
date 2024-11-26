
# How to Run the Project

## 1. Clone the Repository

Clone the repository to your local machine:

```sh
git clone <repository_url>
cd <repository_directory>
```

---

## 2. Set Up the Virtual Environment

Create a virtual environment for the project:

```sh
python3 -m venv venv
```

---

## 3. Activate the Virtual Environment

### For macOS/Linux:

```sh
source venv/bin/activate
```

### For Windows:

```sh
venv\Scriptsctivate
```

---

## 4. Set Up the Environment Variables

Before running the server, you need to create a `.env` file in the root directory of the project. This file will store sensitive information like your database credentials and secret keys.

Here’s a template for your `.env` file:

```
# Django Settings
DATABASE_URL='your_database_url_here'
SECRET_KEY='your_secret_key_here'
DEBUG=False / True

# Gmail Configuration
GMAIL_PASSWORD='your_gmail_password_here'
GMAIL_ACCOUNT='your_gmail_account_here'

# MongoDB Configuration
MONGO_USER='your_mongo_username_here'
MONGO_PASSWORD='your_mongo_password_here'
```

---

## 5. Install Dependencies

After activating the virtual environment, install the required dependencies:

```sh
pip install -r requirements.txt
```

---

## 6. Run Database Migrations

Run the migrations to set up the database:

```sh
python manage.py migrate
```

---

## 7. Run the Development Server

Now you can start the server:

```sh
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) by default.

---

## Alternative: Running the Project with Docker

If you prefer to run the project using Docker, you can skip setting up the virtual environment and run the project using Docker Compose.

### 1. Build and Start the Docker Containers

Run the following command to start the project with Docker Compose:

```sh
docker-compose up -d
```

This will build the Docker images (if not already built) and start the containers in detached mode.

### 2. Access the Project

Once the containers are up and running, you can access the application at [http://localhost:8000/](http://localhost:8000/).

---


