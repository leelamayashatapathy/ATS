import os
import django
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atsconfig.settings') 
django.setup()

from ats.models import Candidate  

def load_data():
    with open('demo.json', 'r') as file:
        candidates = json.load(file)

    for entry in candidates:
        Candidate.objects.get_or_create(**entry)

    print("Data loaded successfully from demo.json")

if __name__ == "__main__":
    load_data()
