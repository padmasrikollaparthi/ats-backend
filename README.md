# ATS Backend (Applicant Tracking System)

This project is a backend implementation of a simple Applicant Tracking System (ATS) built using Flask and SQLAlchemy.  
It demonstrates backend concepts such as REST APIs, role-based access control, application state management using a state machine, audit logging with database transactions, and background task processing using Celery and Redis.

The project is intentionally minimal and focused on backend architecture rather than frontend or production-ready authentication.

---

## Features Implementes

### User Roles (RBAC)
- Users have roles such as `candidate` and `recruiter`
- Role-Based Access Control (RBAC) is enforced using a custom Flask decorator
- Authorization is simulated using an HTTP header (`X-User-Id`)

**Permissions**
- Recruiter:
  - Create jobs
  - Update jobs
  - Delete jobs
  - Change application state
- Candidate:
  - View jobs
  - Apply for jobs

RBAC logic is implemented in:
app/services/authz.py
---
### Job Management
- Create a job (recruiter only)
- List all jobs
- View job details
- Update a job (recruiter only)
- Delete a job (recruiter only)
---
### Job Applications
- Candidates can apply for jobs
- Each application has a status
- Status transitions are validated using a centralized state machine
---
### Application State Machine
- All valid transitions are defined in one place
- Invalid transitions are rejected
Supported states:
applied → screening → interview → offer → hired
Any state → rejected
Implemented in:
app/services/state_machine.py
---
### Application State Audit Logging (Transactional)
- Every application state change is recorded in an audit table
- Each audit record stores:
  - Previous state
  - New state
  - Timestamp
- State update and audit log insertion are wrapped inside a single database transaction to ensure atomicity
Audit model:
ApplicationHistory
---
### Background Email Notifications
- Email notifications are simulated using Celery
- Redis is used as the message broker
- Background processing prevents blocking API requests
Celery task:
send_email_task
---
## Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Celery
- Redis
- Docker (used for Redis)
---

## Project Structure
ats-backend/
├── app/
│ ├── routes/
│ │ ├── auth_routes.py
│ │ ├── job_routes.py
│ │ ├── application_routes.py
│ │ └── ping_routes.py
│ ├── services/
│ │ ├── authz.py
│ │ ├── background_tasks.py
│ │ ├── email_service.py
│ │ └── state_machine.py
│ ├── config.py
│ ├── models.py
│ └── init.py
├── run.py
├── celery_worker.py
├── requirements.txt
├── Dockerfile
├── ats.db
└── README.md
---
## Setup Instructions
### 1. Clone Repository
```bash
git clone <your-github-repo-url>
cd ats-backend

2. Create and Activate Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate

Linux / macOS
python -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Flask Application
python run.py

Application URL:
http://127.0.0.1:5000

Database
SQLite database (ats.db)
Tables are created automatically
Models are defined in:
app/models.py
Running Redis (Required for Celery)
docker run -p 6379:6379 --name ats-redis redis:7
If Redis container already exists:
docker start ats-redis
Running Celery Worker (Windows)
Activate virtual environment:
venv\Scripts\activate
Start Celery worker:
celery -A app.services.background_tasks.celery worker --loglevel=info -P solo
Note:
-P solo is required on Windows
Celery is used only for simulating background email notifications
API Examples
Create Job (Recruiter Only)
curl -X POST http://127.0.0.1:5000/jobs/ \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{"title":"Backend Developer","description":"Flask role"}'

Apply for Job
curl -X POST http://127.0.0.1:5000/applications/ \
-H "Content-Type: application/json" \
-d '{"candidate_name":"Padma","candidate_email":"padma@test.com","job_id":1}'

Change Application Status (Recruiter Only)
curl -X POST http://127.0.0.1:5000/applications/1/transition \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{"to_state":"screening"}'

View Application History
curl http://127.0.0.1:5000/applications/1/history

Limitations
Authentication is simulated using headers and is not production-ready
Email sending is mocked
Dockerfile runs only Flask (Redis and Celery are started separately)
Input validation is minimal

Summary
This project demonstrates:
Clean Flask backend architecture
Role-Based Access Control (RBAC)
Centralized state machine logic
Transactional audit logging
Asynchronous background processing using Celery and Redis
The focus is on backend correctness and design principles rather than full production deployment.

Note: The application is partially containerized. Flask runs via Dockerfile,
while Redis and Celery are started separately for simplicity.
(ATS backend with RBAC, audit logging, and Celery)
