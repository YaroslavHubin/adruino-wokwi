CREATE TABLE climate_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    co2 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
