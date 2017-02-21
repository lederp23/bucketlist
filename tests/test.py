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
        payload={'username':'oliverd', 'password':'munlazd', 'email': 'a@b.cd'}
        response = requests.get('http://127.0.0.1:5000/auth/register', data=payload)
        print(response)
        response = requests.get('http://127.0.0.1:5000/auth/login', data=payload)
        print(response)
        response = requests.get('http://127.0.0.1:5000/auth/token', data=payload)
        print(response.content)
        token = response.content
        payload={'limit':20, 'q': ''}
        response = requests.get('http://127.0.0.1:5000/bucketlist/api/v1.0/bucketlists/',data=payload, headers={'Authorization': token})
        print(response)
        self.assertEqual(response.status_code, 200)
