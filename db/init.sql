CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL,
    tool VARCHAR(50),
    file_path TEXT,
    line_number INTEGER,
    date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'open'
);