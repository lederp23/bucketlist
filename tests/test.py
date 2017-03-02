import urllib, time
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
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
        app.register_blueprint(urls)
        db.create_all()
        self.test_app = app.test_client()

    def tearDown(self):
        os.remove('test.db')

    def test_registration(self):
        """Tests for user registration"""
        #asserts status code 400 if username or password is blank
        payload = {'username': '', 'password': '', 'email': ''}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        self.assertEqual(response.status_code, 400)

        #asserts error if email is invalid
        payload = {'username': 'lederp', 'password': 'lederp', 'email': 'email'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'invalid email')

        #asserts error if username is invalid
        payload = {'username': 'lederp*#', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'username cannot have special characters')

        #asserts status code 400 if username or password is not sent in request
        response = self.test_app.get("/api/v1/auth/register")
        self.assertEqual(response.status_code, 400)

        #asserts that the user has been registered
        payload = {'username': 'lederp1', 'password': 'lederp1',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        self.assertEqual(response.status_code, 200)

        #asserts that the user already exists
        payload = {'username': 'lederp1', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'user already exists')

    def test_login(self):
        """Tests for login"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)

        #asserts status code 400 if form data is not sent in request
        response = self.test_app.get("/api/v1/auth/login")
        self.assertEqual(response.status_code, 400)

        #asserts that the request is successful
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['result'])
        self.assertEqual(response.status_code, 200)

        #asserts user is not authorized with wrong password
        payload = {'username': 'lederp', 'password': 'leder',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        self.assertEqual(response.status_code, 401)

        #asserts that a non-existant user cannot login
        payload = {'username': 'oliver', 'password': 'leder',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        self.assertEqual(response.status_code, 404)

    def test_add_bucketlist(self):
        """Tests for adding a bucketlist"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))

        #asserts a user is authorized
        self.assertTrue(data['result'])

        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}

        #asserts that a bucketlist has been added
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlist']['name'], 'bucketlist1')

        #asserts bad request if name of bucketlist is not provided
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers)
        self.assertEqual(response.status_code, 400)

        #asserts a user cannot add a bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)

        #asserts a user cannot add a bucketlist without token
        headers={'token': 'wrong token'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      data=payload)
        self.assertEqual(response.status_code, 401)

        #asserts a user cannot add a bucketlist with expired token
        time.sleep(3)
        headers={'token': token}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)

    def test_get_bucketlists(self):
        """Tests for getting bucketlists"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}

        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers)
        data = json.loads(response.get_data(as_text=True))

        #asserts that bucketlists are returned
        self.assertTrue(len(data['bucketlists']) > 0)

        #asserts a user cannot get bucketlists with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts searching with wrong name
        headers={'token': token}
        query = {'q': 'reefef'}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 0)

        #asserts searching with correct name, offest and limit
        headers={'token': token}
        query = {'q': 'bucketlist', 'limit': 1, 'offset': 0}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 1)
        headers={'token': token}

        #asserts searching with correct name and limit and wrong offest
        query = {'q': 'bucketlist', 'limit': 1, 'offset': 1}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 0)

        payload = {'name': 'bucketlist2'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)

        #asserts limiting number of bucketlists
        query = {'limit': 1}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 1)

        query = {'limit': 2}
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers, query_string=query)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data['bucketlists']) == 2)

    def test_get_bucketlist(self):
        """Tests getting a single bucketlist"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}

        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        response = self.test_app.get("/api/v1/bucketlists/1",\
                                     headers=headers)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the bucketlist is returned
        self.assertEqual(data['bucketlist']['name'], 'bucketlist1')

        #asserts a user cannot get a bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.get("/api/v1/bucketlists/1",\
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts status_code 404 if bucketlist is not found
        headers={'token': token}
        response = self.test_app.get("/api/v1/bucketlists/4",\
                                     headers=headers)
        self.assertEqual(response.status_code, 404)


    def test_update_bucketlist(self):
        """Tests updating a bucketlist"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        payload = {'name': 'bucketlist2'}
        response = self.test_app.put("/api/v1/bucketlists/1",\
                                     headers=headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the bucketlist is updated
        self.assertTrue(data['result'])

        #asserts a user cannot update bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.put("/api/v1/bucketlists/1",\
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts status_code 404 if bucketlist is not found
        headers={'token': token}
        response = self.test_app.put("/api/v1/bucketlists/6",\
                                     headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        """Tests deleting a bucketlist"""
        payload = {'username': 'lederp', 'password':\
                   'lederp', 'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        response = self.test_app.delete("/api/v1/bucketlists/1",\
                                        headers=headers)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the bucketlist is deleted
        self.assertTrue(data['result'])

        #asserts a user cannot delete bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.delete("/api/v1/bucketlists/1",\
                                        headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts status_code 404 if bucketlist is not found
        headers={'token': token}
        response = self.test_app.delete("/api/v1/bucketlists/6",\
                                        headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_add_item(self):
        """Tests for adding an item to a bucketlist"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        response = self.test_app.post("/api/v1/bucketlists/1/items/",\
                                      headers=headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the item has been added
        self.assertEqual(data['item']['name'], 'item1')

        #asserts bad request if name of item is not provided
        response = self.test_app.post("/api/v1/bucketlists/1/items/",\
                                      headers=headers)
        self.assertEqual(response.status_code, 400)

        #asserts a user cannot add an item with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",\
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 401)

        #asserts a user cannot add an item with bucketlist id
        headers={'token': token}
        response = self.test_app.post("/api/v1/bucketlists/5/items/",\
                                      headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

        #asserts the item is assocaited with that bucketlist
        response = self.test_app.get("/api/v1/bucketlists/1",\
                                     headers=headers)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlist']['items'][0]['name'], 'item1')
        response = self.test_app.get("/api/v1/bucketlists/",\
                                     headers=headers)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['bucketlists'][0]['items'][0]['name'], 'item1')

    def test_update_item(self):
        """Tests updating a bucketlist item"""
        payload = {'username': 'lederp', 'password': 'lederp', 'email':\
                   'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",\
                                      headers=headers, data=payload)
        payload = {'name': 'item2'}
        response = self.test_app.put("/api/v1/bucketlists/1/items/1",\
                                     headers=headers, data=payload)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the item is updated
        self.assertEqual(data['item']['name'], 'item2')

        #asserts a user cannot update bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.put("/api/v1/bucketlists/1/items/1",\
                                     headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts status_code 404 if bucketlist is not found
        headers={'token': token}
        response = self.test_app.put("/api/v1/bucketlists/6/items/1",\
                                     headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

        #asserts status_code 404 if item is not found
        response = self.test_app.put("/api/v1/bucketlists/1/items/6",\
                                     headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        """Tests deleting a bucketlist item"""
        payload = {'username': 'lederp', 'password': 'lederp',\
                   'email': 'lederp@gmail.com'}
        response = self.test_app.get("/api/v1/auth/register", data=payload)
        response = self.test_app.get("/api/v1/auth/login", data=payload)
        data = json.loads(response.get_data(as_text=True))
        token = data['access_token']
        headers={'token': token}
        payload = {'name': 'bucketlist1'}
        response = self.test_app.post("/api/v1/bucketlists/",\
                                      headers=headers, data=payload)
        payload = {'name': 'item1'}
        response = self.test_app.post("/api/v1/bucketlists/1/items/",\
                                      headers=headers, data=payload)
        response = self.test_app.delete("/api/v1/bucketlists/1/items/1",\
                                        headers=headers)
        data = json.loads(response.get_data(as_text=True))

        #asserts that the item is deleted
        self.assertTrue(data['result'])

        #asserts a user cannot delete bucketlist with wrong token
        headers={'token': 'wrong token'}
        response = self.test_app.delete("/api/v1/bucketlists/1/items/1",\
                                        headers=headers)
        self.assertEqual(response.status_code, 401)

        #asserts status_code 404 if bucketlist is not found
        headers={'token': token}
        response = self.test_app.delete("/api/v1/bucketlists/6/items/1",\
                                        headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

        #asserts status_code 404 if item is not found
        response = self.test_app.delete("/api/v1/bucketlists/1/items/6",\
                                        headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)
