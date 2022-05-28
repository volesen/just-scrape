CREATE TABLE IF NOT EXISTS restaurants (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slogan TEXT,
    /* Location info */
    street TEXT NOT NULL,
    postal_code INTEGER NOT NULL,
    city TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    restaurant_id TEXT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    restaurant_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);