Setup
-----
The application works in Python 2.7 and 3.X. <br/>
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
  - [POST /createProduct](#post-createproduct)
  - [GET /getProduct/[id]](#get-getproductid)
  - [GET /getProductByName/[name]](#get-getproductbynamename)	
  - [GET /getAllProducts/[orderby]](#get-getallproductsorderby)
  - [POST /updateProductPrice](#post-updateproductprice)
  - [POST /deleteProduct](#post-deleteproduct)
  - [POST /likeProduct](#post-likeproduct)
  - [POST /buyProduct](#post-buyproduct)
  - [POST /salesLog](#post-saleslog)
  
  
  
  
  
  
  
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
Right response returns a token for authorization headers.<br>
The token was configured to expire in 30 minutes. <br/>
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

### POST /createProduct
Example: http://example.com/api/v1/createProduct

Request body:

	{
	   "name" : "iPhone X",
	   "npc" : "123456",
	   "stock" : "10",
	   "price" : "19900"
	}
> Authorization header: [token]
  
 Good response: <br />
 
	{
	   "success": "A new product has been created!"
	}
  
> Code: `201 Created` <br />

### GET /getProduct/[id]
  
Example: http://example.com/api/v1/getProduct/[id]

  
 Good response: <br />
 
	{
	   "Name": "iPhone X",
	    "Price": "19900",
	    "NPC": "123456",
	    "last_update": "2018-09-15 17:21:12.907826+00:00",
	    "likes": 0,
	    "id": 1,
	    "Stock": "10"
	}
  
> Code: `200 OK` <br />

### GET /getProductByName/[name]
  
Example: http://example.com/api/v1/getProductByName/iPhone

  
 Good response: <br />
 
	{
	   "Name": "iPhone X",
	    "Price": "19900",
	    "NPC": "123456",
	    "last_update": "2018-09-15 17:21:12.907826+00:00",
	    "likes": 0,
	    "id": 1,
	    "Stock": "10"
	}
  
> Code: `200 OK` <br />

### GET /getAllProducts/[orderby]
* There are 2 parameters avalible:
	* name
	* likes
Example: http://example.com/api/v1/getAllProducts/name

  
 Good response: <br />
 
	{
	      	"Name": "iPhone 8",
		"Price": "12500",
		"NPC": "123455",
		"last_update": "2018-09-15 17:21:12.907826+00:00",
		"likes": 0,
		"id": "2",
		"Stock": "10"
	}
	{
	  	"Name": "iPhone X",
	   	"Price": "19900",
	   	"NPC": "123456",
	   	"last_update": "2018-09-15 17:21:12.907826+00:00",
	   	"likes": 0,
	   	"id": 1,
	   	"Stock": "10"
	}
  
> Code: `200 OK` <br />

### POST /updateProductPrice

Example: http://example.com/api/v1/updateProductPrice

Request body:

	{
	   "id" : "1",
	   "price" : "20000",
	}
> Authorization header: [token]
  
 Good response: <br />
 
	{
	   "success": "Product has been updated!"
	}
  
> Code: `200 OK` <br />

### POST /deleteProduct

Example: http://example.com/api/v1/deleteProduct

Request body:

	{
	   "id" : "1",
	}
> Authorization header: [token]
  
 Good response: <br />
 
	{
	   "success": "Product has been deleted!"
	}
  
> Code: `200 OK` <br />



### POST /likeProduct
For this operation the user must be "registered" kind. <br/>
Example: http://example.com/api/v1/likeProduct

Request body:

	{
	   "productId" : "1",
	}
> Authorization header: [token]
  
 Good response: <br />
 
	{
	   "success": "Like Saved!"
	}
  
> Code: `200 OK` <br />


### POST /buyProduct
For this operation the user must be "registered" kind. <br/>
Example: http://example.com/api/v1/buyProduct

Request body:

	{
	   "productId" : "1",
	   "quantity" : "1"
	}
> Authorization header: [token]
  
 Good response: <br />
 
	{
	   "success": "Purchase made successfully"
	}
  
> Code: `200 OK` <br />


### POST /salesLog
For this operation the user must be "admin" kind. <br/>
Example: http://example.com/api/v1/salesLog

Request body:

> Authorization header: [token]
  
 Good response: <br />
 it returns a log about all sales made.
 
	{
	   	"product": "iPhone X",
		"price": "6000",
		"buyer": "registered",
		"date": "2018-09-15 18:28:19.363505+00:00",
		"total": "6000.0",
		"id": 1,
		"quantity": 1
	}
  
> Code: `200 OK` <br />




## Live Demo 🚀
You can check the live demo deployed on Heroku here:
```
https://e-commerc-test.herokuapp.com/api/v1
```


## Test in Postman
You can test the app easily using [Postman](https://www.getpostman.com/) importing the [E-commerce.postman_collection.json](https://github.com/3vilware/E-commerce-API/blob/master/E-commerce.postman_collection.json) file.
