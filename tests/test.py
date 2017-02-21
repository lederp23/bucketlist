import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from unittest import TestCase
from app import app
import requests
from config import ProductionConfig
import os
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/bucketlist.db'

class TestApi(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_bucketlists(self):
        payload={'username':'oliver', 'password':'munlaz', 'email': 'a@b.c'}
        response = requests.get('http://127.0.0.1:5000/auth/register', json=payload)
        print(response)
        response = requests.get('http://127.0.0.1:5000/auth/login', json=payload)
        print(response)
        response = requests.get('http://127.0.0.1:5000/auth/token', json=payload)
        print(response)
        response = requests.get('http://127.0.0.1:5000/bucketlist/api/v1.0/bucketlists/')
        print(response)
        self.assertEqual(response.status_code, 201)
