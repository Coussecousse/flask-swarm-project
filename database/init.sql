-- Database initialization script
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, description) VALUES
    ('Sample Item 1', 'This is a sample item'),
    ('Sample Item 2', 'Another sample item'),
    ('Sample Item 3', 'Yet another sample')
ON CONFLICT DO NOTHING;