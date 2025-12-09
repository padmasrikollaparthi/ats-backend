ATS Backend

A simple Applicant Tracking System (ATS) Backend built with Flask, SQLAlchemy, Celery, and Redis. This backend supports user authentication, job management, and job applications with state transitions.

Features
Authentication
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Login an existing user
Job Management
Method	Endpoint	Description
POST	/jobs/create	Create a new job
GET	/jobs/list	List all jobs
GET	/jobs/<id>	View job details
PUT	/jobs/<id>	Update job
DELETE	/jobs/<id>	Delete job
Applications
Method	Endpoint	Description
POST	/applications/create	Apply for a job
POST	/applications/change-status	Change application state (shortlisted → selected)
Installation

Clone the repository:

git clone <your-repo-url>
cd ats-backend


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac


Install dependencies:

pip install -r requirements.txt

Database

SQLite database is used (ats.db).

Models are defined in app/models.py.

Run the app to automatically create the database tables.

Running the Application

Start the Flask app:

python run.py


Access the app at:

http://127.0.0.1:5000

Celery (Background Tasks)

Celery is used for asynchronous tasks such as sending emails.

Ensure Redis is running:

docker run -p 6379:6379 --name ats-redis redis:7


Start the Celery worker:

venv\Scripts\activate
celery -A app.services.background_tasks.celery worker --loglevel=info -P solo

Project Structure
ats-backend/
├── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── job_routes.py
│   │   ├── application_routes.py
│   │   └── ping_routes.py
│   ├── services/
│   │   ├── background_tasks.py
│   │   ├── email_service.py
│   │   └── state_machine.py
│   ├── config.py
│   ├── models.py
│   └── __init__.py
├── venv/
├── run.py
├── celery_worker.py
├── Dockerfile
├── requirements.txt
├── ats.db
├── README.md

API Testing

You can test endpoints using curl or Postman. Example:

curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"email":"padma@example.com","role":"candidate"}'

Notes

Windows users should run Celery with the -P solo option due to multiprocessing issues.

Redis is required for Celery tasks.

