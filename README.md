Setup
-----
You can install the dependencies using pip under clone repository:

	$ pip install -r requirements.txt
  
  
Run
-----
Type on project root:

	$ python manage.py runserver
  
* By default the app runs in:
    * http://localhost:8000
    * The API works under /api/v1 path.


## Requests & Responses Examples

### API Resources

  - [POST /createUser](#post-createuser)
  - [POST /loguin](#post-loguin)
  
  
### POST /createUser
* There are 2 kinds of user:
  * Admin = 1
  * Registered = 2
  
Example: http://example.com/api/v1/createUser

Request body:

	{
	   "user" : "username",
	   "password" : "mypass",
	   "repeat" : "mypass",
	   "kind" : "1"
	}
  
 Good response: <br />
 
	{
	   "success": "User created successfully"
	}
  
> Code: `201 Created` <br />

### POST /loguin
Right response returns a token for authorization headers. <br/>
Example: http://example.com/api/v1/loguin


Request body:

	{
	   "user" : "username",
	   "password" : "mypass"
	}

Good response: <br />
 
	{
	    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImV4cCI6MTUzNzAyODkwNH0.ttyFoOfY4MCQqcLsUjf-hkATulGXp81lJ4sXGZvCuQg"
	}
  
> Code: `202 Accepted` <br />
