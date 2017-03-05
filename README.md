----
BucketList is an API that allows users to sign up and add bucketlists which are things that they wish to do in the future. The user can also add an item to a bucketlist. Both bucketlists and items can be updated or deleted.
----

**Register User**
----
  Adds a user and returns the username.

* **URL**

  /api/<version>/auth/register

* **Method:**

  `POST`

*  **URL Params**

    **Required:**

    `version=[string]`

* **Data Params**

    **Required:**

    `username=[string]`
    `email=[string]`
    `password=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ username : "derp" }`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />

  OR

  * **Content:** {'error': 'invalid email'}

  OR

  * **Content:** {'error': 'username cannot have special characters'}

  OR

  * **Content:** {'error': 'user already exists'}


* **Sample Call:**

  ```python
  payload = {'username': 'lederp', 'password': 'lederp', 'email': 'lederp@example.com'}
  post("/api/v1/auth/register", data=payload)
  ```

----

**Login User**
----
  Returns authentication token.

* **URL**

  /api/<version>/auth/login

* **Method:**

  `POST`

*  **URL Params**

    **Required:**

    `version=[string]`

* **Data Params**

    **Required:**

    `username=[string]`
    `password=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{'result': True, 'token' : "eyJpYXQiOjE0ODg3MDUzMzMsImV4cCI6MTQ4ODcwNTkzMy" }`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />

  OR

  * **Code:** 404 NOT FOUND <br />

  OR

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Content:** {'error': 'username cannot have special characters'}

  OR

  * **Content:** {'error': 'user already exists'}


* **Sample Call:**

  ```python
  payload = {'username': 'lederp', 'password': 'lederp'}
  post("/api/v1/auth/login", data=payload)
  ```

----

**Get bucketlists**
----
  Returns bucketlists.

* **URL**

  /api/<version>/bucketlists/

* **Method:**

  `GET`

*  **URL Params**

    **Required:**

    `version=[string]`

    **Optional:**

    `q=[string]`
    `limit=[integer]`
    `offset=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ `<br />
    `                 "bucketlists": [  `<br />
    `                    {`
    `                      "created_by": "wewe1",  `<br />
    `                      "date_created": "Sat, 04 Mar 2017 09:46:04 GMT",`<br />
    `                      "date_modified": "Sat, 04 Mar 2017 09:46:04 GMT",`  <br />
    `                      "id": 6,  `<br />
    `                      "items": [],`  <br />
    `                      "name": "bucketlist1"  `<br />
    `                    },  `<br />
    `                    {  `<br />
    `                      "created_by": "wewe1",  `<br />
    `                      "date_created": "Sat, 04 Mar 2017 09:46:06 GMT",`<br />  
    `                      "date_modified": "Sat, 04 Mar 2017 09:46:06 GMT",  `<br />
    `                      "id": 7,  `<br />
    `                      "items": [],  `<br />
    `                      "name": "bucketlist1" `<br />
    `                      ],  `<br />
    `                   "next_url": "/api/v1/bucketlists/?q=buck&limit=2&offset=2", `<br />
    `                   "previous_url": ""  `<br />
    `                 }`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  get("/api/v1/bucketlists/", headers=header)
  ```

----

**Get bucketlist**
----
  Returns a bucketlist.

* **URL**

  /api/<version>/bucketlists/<id>

* **Method:**

  `GET`

*  **URL Params**

    **Required:**

    `version=[string]`
    `id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{`<br />
    `                  "bucketlist": {`<br />
    `                    "created_by": "wewe1",`<br />
    `                    "date_created": "Sat, 04 Mar 2017 09:45:54 GMT",`<br />
    `                    "date_modified": "Sat, 04 Mar 2017 09:45:54 GMT",`<br />
    `                    "id": 2,`<br />
    `                    "items": [`<br />
    `                      {`
    `                        "date_created": "Sat, 04 Mar 2017 09:46:20 GMT",`<br />
    `                        "date_modified": "Sat, 04 Mar 2017 09:46:20 GMT",`<br />
    `                        "done": false,`<br />
    `                        "id": 1,`<br />
    `                        "name": "you"`<br />
    `                      }`<br />
    `                 }`<br />


* **Error Response:**

  * **Code:** 404 NOT FOUND <br />

  OR

  * **Code:** 401 UNAUTHORIZED <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  get("/api/v1/bucketlists/2", headers=header)
  ```

----

**Add bucketlist**
----
  Adds a bucketlist and returns it.

* **URL**

  /api/<version>/bucketlists/

* **Method:**

  `POST`

*  **URL Params**

    `version=[string]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{`<br />
    `                  "bucketlist": {`<br />
    `                    "created_by": "wewe2",`<br />
    `                    "date_created": "Sun, 05 Mar 2017 09:57:56 GMT",`<br />
    `                    "date_modified": "Sun, 05 Mar 2017 09:57:56 GMT",`<br />
    `                    "id": 25,`<br />
    `                    "items": [],`<br />
    `                    "name": "wewe na mimi"`<br />
    `                  }`<br />
    `                }`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  payload = ('name': 'wewe na mimi')
  post("/api/v1/bucketlists/", data=payload, headers=header)
  ```

----

**Update bucketlist**
----
  Changes the name of the bucketlist and returns True.

* **URL**

  /api/<version>/bucketlists/<id>

* **Method:**

  `PUT`

*  **URL Params**

    `version=[string]`
    `id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 'result': True }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  payload = ('name': 'wewe na yeye')
  post("/api/v1/bucketlists/", data=payload, headers=header)
  ```

----

**Delete bucketlist**
----
  Deletes a bucketlist and returns True.

* **URL**

  /api/<version>/bucketlists/<id>

* **Method:**

  `DELETE`

*  **URL Params**

    `version=[string]`
    `id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 'result': True }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  payload = ('name': 'wewe na yeye')
  delete("/api/v1/bucketlists/", headers=header)
  ```

----

**Add bucketlist item**
----
  Adds a bucketlist item and returns it.

* **URL**

  /api/<version>/bucketlists/<id>/items/

* **Method:**

  `POST`

*  **URL Params**

    `version=[string]`
    `id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{`<br />
    `                  "item": {`<br />
    `                    "bucketlist_id": 2,`<br />
    `                    "date_created": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    `                    "date_modified": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    `                    "done": false,`<br />
    `                    "id": 5,`<br />
    `                    "name": "wewe na mimi sasa"`<br />
    `                  }`<br />
    `                }`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  payload = ('name': 'wewe na mimi sasa')
  post("/api/v1/bucketlists/2/items/", data=payload, headers=header)
  ```

----

**Update bucketlist item**
----
  Updates a bucketlist item and returns it.

* **URL**

  /api/<version>/bucketlists/<id>/items/<item_id>

* **Method:**

  `PUT`

*  **URL Params**

    `version=[string]`
    `id=[integer]`
    `item_id=[integer]`

* **Data Params**

    **Required:**

    `name=[string]`

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{`<br />
    `                  "item": {`<br />
    `                    "date_created": "Sun, 05 Mar 2017 10:14:13 GMT",`<br />
    `                    "date_modified": "Sun, 05 Mar 2017 10:17:37 GMT",`<br />
    `                    "done": false,`<br />
    `                    "id": 5,`<br />
    `                    "name": "wewe na mimi tena"`<br />
    `                  }`<br />
    `                }`<br />

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  payload = ('name': 'wewe na mimi tena', 'done': True)
  put("/api/v1/bucketlists/2/items/5", data=payload, headers=header)
  ```

----

**Delete bucketlist item**
----
  Deletes a bucketlist item and returns True.

* **URL**

  /api/<version>/bucketlists/<id>/items/<item_id>

* **Method:**

  `DELETE`

*  **URL Params**

    `version=[string]`
    `id=[integer]`
    `item_id=[integer]`

* **Data Params**

    **Required:**

    None

* **Header Params**

    **Required:**

    `token=[string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 'result': True }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />

  OR

  * **Code:** 404 NOT FOUND <br />

* **Sample Call:**

  ```python
  header = {'token': 'adefeffssddrr4f3'}
  delete("/api/v1/bucketlists/2/items/5", headers=header)
  ```
