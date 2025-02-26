CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL,
    tool VARCHAR(50) NOT NULL,
    file_path TEXT,
    line_number INT,
    date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);
