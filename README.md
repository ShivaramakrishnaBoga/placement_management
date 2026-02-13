# Modern Institutional Placement Governance Platform

An API-first Placement Governance app built with Django & DRF.
Status: Implemented Core Features, API, and Dashboard basics.

## Features
- **Smart Eligibility Engine**: Validates CGPA, Backlogs, Branch, Policy.
- **Offer Policy Engine**: Tracks Dream/Super Dream offers.
- **Academic Master Data**: Admin Excel upload (API).
- **Application Workflow**: Applied -> Shortlisted -> Selected -> Rejected.
- **Analytics API**: Dashboard metrics via `/api/analytics/`.

## Setup
1. Create venv: `python -m venv venv`
2. Activate: `./venv/Scripts/activate`
3. Install: `pip install -r requirements.txt`
4. Migrate: `python manage.py migrate`
5. Create Admin: `python create_admin.py` (User: `admin`, Pass: `admin`)
6. Run: `python manage.py runserver`

## API Endpoints
- `/api/jobs/`: List Job Drives (GET), Create (POST - Admin)
- `/api/students/`: Profile Management
- `/api/applications/`: Manage Applications
- `/api/analytics/`: Admin Dashboard JSON

## Usage
- Login as Admin to `/admin` to manage Job Drives and view Analytics.
- Login as Student (create via Admin or Register page) to view Jobs and Apply.
