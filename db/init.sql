CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    description TEXT
);

-- Генерация 50 тестовых товаров
DO $$
BEGIN
    FOR i IN 1..50 LOOP
        INSERT INTO products (name, price, description)
        VALUES (
            'Product ' || i,
            (10 + random() * 90)::numeric(10,2),
            'Description for product ' || i
        );
    END LOOP;
END $$;