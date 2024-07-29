CREATE DATABASE api_pizzas;
USE api_pizzas;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('cliente', 'empleado') NOT NULL DEFAULT 'cliente',
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE pizzas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE pizza_ingredients (
    pizza_id INT,
    ingredient_id INT,
    PRIMARY KEY (pizza_id, ingredient_id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2),
    address TEXT,
    status ENUM('pending', 'preparing', 'delivered'),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    order_id INT,
    pizza_id INT,
    quantity INT,
    PRIMARY KEY (order_id, pizza_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (pizza_id) REFERENCES pizzas(id)
);

USE pizza_app;

-- Insertar usuarios
INSERT INTO users (username, password, email, role)
VALUES
    ('john_doe', 'password123', 'johndoe@example.com', 'cliente'),
    ('jane_smith', 'pass456', 'janesmith@example.com', 'empleado'),
    ('admin', 'admin123', 'admin@example.com', 'empleado'),
    ('customer1', 'pass789', 'customer1@example.com', 'cliente');

-- Insertar pizzas
INSERT INTO pizzas (name, price)
VALUES
    ('Margherita', '', 10.99),
    ('Pepperoni', 12.99),
    ('Vegetarian', 11.49),
    ('Hawaiian', 13.99);

-- Insertar ingredientes
INSERT INTO ingredients (name)
VALUES
    ('Tomate'),
    ('Queso mozzarella'),
    ('Pepperoni'),
    ('Pimiento');

-- Insertar relación pizza-ingredientes (ejemplo para la pizza Margherita)
INSERT INTO pizza_ingredients (pizza_id, ingredient_id)
VALUES
    ((SELECT id FROM pizzas WHERE name = 'Margherita'), (SELECT id FROM ingredients WHERE name = 'Tomate')),
    ((SELECT id FROM pizzas WHERE name = 'Margherita'), (SELECT id FROM ingredients WHERE name = 'Queso mozzarella'));

-- Insertar pedidos
INSERT INTO orders (user_id, total_price, address)
VALUES
    ((SELECT id FROM users WHERE username = 'john_doe'), 10.99, 'Calle Falsa 123'),
    ((SELECT id FROM users WHERE username = 'jane_smith'), 15.98, 'Avenida Principal 456'),
    ((SELECT id FROM users WHERE username = 'customer1'), 12.99, 'Calle Secundaria 789'),
    ((SELECT id FROM users WHERE username = 'john_doe'), 13.99, 'Calle Falsa 123');

-- Insertar items de un pedido (ejemplo para el primer pedido de John Doe)
INSERT INTO order_items (order_id, pizza_id, quantity)
VALUES
    ((SELECT id FROM orders WHERE user_id = (SELECT id FROM users WHERE username = 'john_doe') ORDER BY id DESC LIMIT 1),
     (SELECT id FROM pizzas WHERE name = 'Margherita'), 1);

drop TABLE pizza_ingredients;
drop TABLE ingredients;
drop TABLE pizzas;
drop TABLE users;
drop TABLE orders_items;
drop TABLE orders;