# APIzza

*Exercise with FastAPI and SQLAlchemy*

---

### API Specifications

The API is designed to include the following key verticals. The endpoints listed are suggested examples, and the HTTP verbs implemented for each can be chosen as needed. All decisions regarding endpoint design should be clearly explained in the README. Additionally, Swagger documentation is required to ensure clear and accessible API documentation.

#### **/api/user:**
- **Authentication:** The API supports user authentication, allowing users to log in, log out, and register with basic credentials (username and password).
  
- **Profile Management:** Users can update their profile information, including essential fields such as phone number, email, and address.
  
- **Administrative Access:** Administrators have access to a comprehensive user list, which includes detailed information on each user, as well as their order history.

#### **/api/orders [Optional Admin Role]:**
- **Order Management:** Orders are displayed chronologically, with the most recent orders appearing first. Each order entry includes all details necessary for operational tasks, such as customer information and delivery specifics.

<!-- - **Pagination [Optional]:** Support for pagination in the order list is optional but recommended for better data management. -->

- **Order Details:** Each order is assigned a unique identifier. The API provides an endpoint for retrieving all relevant details about a specific order using this identifier.

#### **/api/pizzas:**
- **Menu Access:** The API allows access to the pizzeria's menu, displaying the name and price of each pizza.

- **Pizza Details:** Detailed information on each pizza, including ingredients and preparation methods, is available to enhance the customer experience and assist in marketing efforts.


---

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
