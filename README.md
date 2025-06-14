# ATS Candidate API

This is a simple REST API built using Django and DRF to manage candidate records for an ATS (Applicant Tracking System). It allows basic CRUD operations and supports searching candidates by name based on how closely they match the search terms.

## Setup Instructions

Make sure you have Python and virtualenv installed. Then do the following:


git clone <your-repo-url>
cd <project-folder>
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt

## DB Migration
python manage.py migrate
## Run Application
python manage.py runserver


## API

http://127.0.0.1:8000/api/candidates/ - The End Point for POST, PUT & DELETE

http://127.0.0.1:8000/api/candidates/search/?q=Ajay Kumar Yadav : - The End Point for serach api



## Demo data
in demo.json file you can find the demodata




