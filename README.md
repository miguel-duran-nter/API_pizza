# APIzza

*Exercise with FastAPI and SQLAlchemy*

---

Must contain at least the following verticals, whose endpoints shown below are only for guidance purposes, the implementation of the http "verbs" for each endpoint will be freely chosen and must be duly justified in the README. Additionally, a Swagger is required:

- /api/user:
    
    - It must allow logging in and out, as well as registering in the application with basic authentication (username and password).
    
    - It must allow editing your profile and updating your data. The minimum required fields will be phone, email and address.
    
    - [Admin only] A complete list of users must be available. The information in this list must contain information related to each user and their order history.

- /api/orders [optional use admin role]:
    
    - Orders must be displayed in order of date and time, with the first to be displayed being the last order to arrive. All relevant details for the activity of the pizzeria must be displayed, such as the data of the customer who bought the pizza and their delivery data.
    
    - [OPTIONAL] It will be considered to provide pagination to the endpoint.
    
    - As each order will need a unique identifier number for its registration, invoice, delivery, etc. A way to consult a specific order with all its details must be provided.

- /api/pizzas:
    
    - A way to access the list of pizzas available on the pizzeria's menu must be provided. This list must contain the name and price of the pizza.
    
    - A way to consult the details of each pizza in terms of ingredients, preparation, etc. will be provided. Any detail that is considered necessary and that helps its marketing.

## Start virtual environment

### Create virtual environment

```Python
python3 -m venv .venv
```

### Run virtual environment

```Python
source .venv/bin/active
```

## Start Uvicorn server

```Bash
uvicorn main:app
```
If you want the server to restart after any change, enter the following command
```Bash
uvicorn main:app --reload
```

## Endpoints

### GET

- '/docs' -> Swager Documentation
- '/users' -> List user, only if you are admin
- '/users/<user_id>' -> Displays the data of the user with the entered id
- '/orders' -> List orders
- '/orders/history/<user_id>' -> Displays the order history of the user with the entered id

### POST

- '/users' -> Register a new user
- '/orders' -> Create a new order
- '/auth/login' -> Log in
- 'auth/logout? -> Log Out

### PUT

- '/orders/<order_id>' -> Updates the order status with the entered id
