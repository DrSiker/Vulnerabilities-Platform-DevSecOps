CREATE TABLE vulnerabilities (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    severity VARCHAR(50) NOT NULL
);