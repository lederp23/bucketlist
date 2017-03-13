import urllib
import time
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from v1.accounts.models import User
from v1.api.models import BucketList, Item
from urls import urls
import json


class MyTest(TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.url_map.strict_slashes = False
        app.register_blueprint(urls)
        db.create_all()
        self.test_app = app.test_client()
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))

        # asserts that a user is authorized
        self.assertTrue(data['result'])

        token = data['access_token']
        self.headers = {'token': token}

        self.payload2 = {'username': 'lederp2', 'password': 'lederp2',
                         'email': 'lederp2@gmail.com'}
        response2 = self.test_app.post(
            "/api/v1/auth/register", data=self.payload2)

    def tearDown(self):
        os.remove('test.db')

    def test_api_version(self):
        """Tests versionin of api"""
        # asserts OK response when api version exists
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        self.assertEqual(response.status_code, 200)

        # asserts status_code 404 when api version does not exist
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v6/auth/register", data=payload)
        self.assertEqual(response.status_code, 404)

    def test_registration(self):
        """Tests for user registration"""
        # asserts status code 400 if username or password is blank
        payload = {'username': '', 'password': '', 'email': ''}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        self.assertEqual(response.status_code, 400)

        # asserts error if email is invalid
        payload = {'username': 'lederp', 'password': 'lederp', 'email': 'email'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'invalid email')

        # asserts error if username is invalid
        payload = {'username': 'lederp*#', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(
            data['error'], 'username cannot have special characters')

        # asserts status code 400 if username or password is not sent in request
        response = self.test_app.post("/api/v1/auth/register")
        self.assertEqual(response.status_code, 400)

        # asserts that the user has been registered
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        self.assertEqual(response.status_code, 200)

        # asserts that the user already exists
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'user already exists')

    def test_login(self):
        """Tests for login"""
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/register", data=payload)

        # asserts error if username is invalid
        payload = {'username': 'lederp*#', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(
            data['error'], 'username cannot have special characters')

        # asserts status code 400 if username or password is blank
        payload = {'username': '', 'password': ''}
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        self.assertEqual(response.status_code, 400)

        # asserts status code 400 if form data is not sent in request
        response = self.test_app.post("/api/v1/auth/login")
        self.assertEqual(response.status_code, 400)

        # asserts that the request is successful
        payload = {'username': 'lederp', 'password': 'lederp',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['result'])
        self.assertEqual(response.status_code, 200)

        # asserts that user is not authorized with wrong password
        payload = {'username': 'lederp', 'password': 'leder',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        self.assertEqual(response.status_code, 401)

        # asserts that a non-existant user cannot login
        payload = {'username': 'oliver', 'password': 'leder',
                   'email': 'lederp@gmail.com'}
        response = self.test_app.post("/api/v1/auth/login", data=payload)
        self.assertEqual(response.status_code, 404)

    def test_add_bucketlist(self):
        """Tests for adding a bucketlist"""
        payload = {'name': 'bucketlist1'}

        # asserts that a bucketlist has been added
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlist']['name'], 'bucketlist1')

        # asserts status_code 404 if name of bucketlist is not provided
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers)
        self.assertEqual(response.status_code, 400)

        # asserts a user cannot add a bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)

        # asserts a user cannot add a bucketlist without token
        response = self.test_app.post("/api/v1/bucketlists/",
                                      data=payload)
        self.assertEqual(response.status_code, 400)

        # asserts a user cannot add a bucketlist with expired token
        time.sleep(3)
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 401)

    def test_get_bucketlists(self):
        """Tests for getting bucketlists"""
        payload = {'name': 'bucketlist1'}

        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers)
        data = json.loads(response.get_data(as_text=True))

        # asserts that bucketlists are returned
        self.assertTrue(len(data['bucketlists']) > 0)

        # asserts a user cannot get bucketlists with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts empty list of bucketlists when searching for missing
        # bucketlist
        query = {'q': 'reefef'}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 0)

        # asserts bucketlist when searching with correct name, offest and limit
        query = {'q': 'bucketlist', 'limit': 1, 'offset': 0}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 1)

        # asserts empty list of bucketlists when searching with wrong offest
        query = {'q': 'bucketlist', 'limit': 1, 'offset': 1}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 0)

        payload = {'name': 'bucketlist2'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)

        # asserts number of bucketlists when limiting number of bucketlists
        query = {'limit': 1}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 1)

        query = {'limit': 2}
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 2)

    def test_get_bucketlist(self):
        """Tests getting a single bucketlist"""
        payload = {'name': 'bucketlist1'}

        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        response = self.test_app.get("/api/v1/bucketlists/1",
                                     headers=self.headers)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the bucketlist is returned
        self.assertEqual(data['bucketlist']['name'], 'bucketlist1')

        # asserts that a user cannot get a bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.get("/api/v1/bucketlists/1",
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts status_code 404 if bucketlist is not found
        response = self.test_app.get("/api/v1/bucketlists/4",
                                     headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_bucketlist(self):
        """Tests updating a bucketlist"""
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        payload = {'name': 'bucketlist2'}
        response = self.test_app.put("/api/v1/bucketlists/1",
                                     headers=self.headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the bucketlist is updated
        self.assertTrue(data['result'])

        # asserts that a user cannot update bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.put("/api/v1/bucketlists/1",
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts status_code 404 if bucketlist is not found
        response = self.test_app.put("/api/v1/bucketlists/6",
                                     headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        """Tests deleting a bucketlist"""
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        response = self.test_app.delete("/api/v1/bucketlists/1",
                                        headers=self.headers)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the bucketlist is deleted
        self.assertTrue(data['result'])

        # asserts a user cannot delete bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.delete("/api/v1/bucketlists/1",
                                        headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts status_code 404 if bucketlist is not found
        response = self.test_app.delete("/api/v1/bucketlists/6",
                                        headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_add_item(self):
        """Tests for adding an item to a bucketlist"""
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        response = self.test_app.post("/api/v1/bucketlists/1/items/",
                                      headers=self.headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the item has been added
        self.assertEqual(data['item']['name'], 'item1')

        # asserts status_code 404 if name of item is not provided
        response = self.test_app.post("/api/v1/bucketlists/1/items/",
                                      headers=self.headers)
        self.assertEqual(response.status_code, 400)

        # asserts that a user cannot add an item with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)

        # asserts that a user cannot add an item without bucketlist id
        response = self.test_app.post("/api/v1/bucketlists/5/items/",
                                      headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)

        # asserts that the item is assocaited with that bucketlist
        response = self.test_app.get("/api/v1/bucketlists/1",
                                     headers=self.headers)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlist']['items'][0]['name'], 'item1')
        response = self.test_app.get("/api/v1/bucketlists/",
                                     headers=self.headers)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlists'][0]['items'][0]['name'], 'item1')

    def test_update_item(self):
        """Tests updating a bucketlist item"""
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",
                                      headers=self.headers, data=payload)
        payload = {'name': 'item2', 'done': True}
        response = self.test_app.put("/api/v1/bucketlists/1/items/1",
                                     headers=self.headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the item is updated
        self.assertEqual(data['item']['name'], 'item2')

        # asserts that a user cannot update bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.put("/api/v1/bucketlists/1/items/1",
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts status_code 404 if bucketlist is not found
        response = self.test_app.put("/api/v1/bucketlists/6/items/1",
                                     headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)

        # asserts status_code 404 if item is not found
        response = self.test_app.put("/api/v1/bucketlists/1/items/6",
                                     headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        """Tests deleting a bucketlist item"""
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",
                                      headers=self.headers, data=payload)
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",
                                      headers=self.headers, data=payload)
        response = self.test_app.delete("/api/v1/bucketlists/1/items/1",
                                        headers=self.headers)
        data = json.loads(response.get_data(as_text=True))

        # asserts that the item is deleted
        self.assertTrue(data['result'])

        # asserts that a user cannot delete bucketlist with wrong token
        headers = {'token': 'wrong token'}
        response = self.test_app.delete("/api/v1/bucketlists/1/items/1",
                                        headers=headers)
        self.assertEqual(response.status_code, 401)

        # asserts status_code 404 if bucketlist is not found
        response = self.test_app.delete("/api/v1/bucketlists/6/items/1",
                                        headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)

        # asserts status_code 404 if item is not found
        response = self.test_app.delete("/api/v1/bucketlists/1/items/6",
                                        headers=self.headers, data=payload)
        self.assertEqual(response.status_code, 404)
