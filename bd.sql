CREATE DATABASE api_pizzas;
USE api_pizzas;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('cliente', 'empleado', 'admin') NOT NULL DEFAULT 'cliente',
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
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    pizza_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
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
INSERT INTO pizzas (image, name, price) VALUES
('pepperoni.jpg', 'Pepperoni', 12.99),
('margherita.jpg', 'Margherita', 10.99),
('bbq_chicken.jpg', 'BBQ Chicken', 14.99);


-- Insertar ingredientes
INSERT INTO ingredients (name) VALUES
('Tomato Sauce'),
('Cheese'),
('Pepperoni'),
('Chicken'),
('BBQ Sauce'),
('Basil');

-- Insertar relación pizza-ingredientes (ejemplo para la pizza Margherita)
-- Pepperoni
INSERT INTO pizza_ingredients (pizza_id, ingredient_id) VALUES
(1, 1), -- Tomato Sauce
(1, 2), -- Cheese
(1, 3); -- Pepperoni

-- Margherita
INSERT INTO pizza_ingredients (pizza_id, ingredient_id) VALUES
(2, 1), -- Tomato Sauce
(2, 2), -- Cheese
(2, 6); -- Basil

-- BBQ Chicken
INSERT INTO pizza_ingredients (pizza_id, ingredient_id) VALUES
(3, 5), -- BBQ Sauce
(3, 2), -- Cheese
(3, 4); -- Chicken


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


SELECT p.name, p.price , ingredients.name as ingredients
FROM pizzas p
JOIN pizza_ingredients ON p.id = pizza_ingredients.pizza_id
JOIN ingredients ON pizza_ingredients.ingredient_id = ingredients.id;
