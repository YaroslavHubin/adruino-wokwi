import mysql.connector

dataset = [
    {"temperature":24.00, "humidity":40.00, "co2":1818.00},
    {"temperature":24.00, "humidity":40.00, "co2":1818.00},
    {"temperature":24.00, "humidity":40.00, "co2":1818.00},
    {"temperature":24.00, "humidity":40.00, "co2":1818.00},
    {"temperature":24.00, "humidity":40.00, "co2":1818.00},
    {"temperature":24.00, "humidity":40.00, "co2":1870.00},
    {"temperature":24.00, "humidity":40.00, "co2":1879.00},
    {"temperature":24.00, "humidity":40.00, "co2":1879.00},
    {"temperature":24.00, "humidity":40.00, "co2":1879.00},
    {"temperature":24.00, "humidity":40.00, "co2":1618.00},
    {"temperature":24.00, "humidity":40.00, "co2":1618.00},
    {"temperature":24.00, "humidity":40.00, "co2":1618.00},
    {"temperature":57.70, "humidity":40.00, "co2":1618.00},
    {"temperature":57.70, "humidity":68.50, "co2":1618.00},
    {"temperature":57.70, "humidity":68.50, "co2":1618.00},
    {"temperature":57.70, "humidity":68.50, "co2":1618.00},
    {"temperature":57.70, "humidity":68.50, "co2":1618.00},
    {"temperature":57.70, "humidity":68.50, "co2":1618.00},
    {"temperature":43.70, "humidity":68.50, "co2":1618.00},
    {"temperature":43.70, "humidity":68.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1618.00},
    {"temperature":43.70, "humidity":59.50, "co2":1979.00},
    {"temperature":43.70, "humidity":59.50, "co2":1979.00},
    {"temperature":80.00, "humidity":59.50, "co2":1979.00},
    {"temperature":80.00, "humidity":59.50, "co2":1979.00},
    {"temperature":80.00, "humidity":4.00, "co2":1979.00},
    {"temperature":80.00, "humidity":3.00, "co2":1979.00},
    {"temperature":80.00, "humidity":3.00, "co2":1979.00},
    {"temperature":80.00, "humidity":3.00, "co2":1979.00},
    {"temperature":80.00, "humidity":3.00, "co2":1979.00},
    {"temperature":49.80, "humidity":3.00, "co2":1979.00},
    {"temperature":49.80, "humidity":64.00, "co2":1979.00},
    {"temperature":49.80, "humidity":64.00, "co2":1655.00},
    {"temperature":49.80, "humidity":64.00, "co2":1655.00},
    {"temperature":49.80, "humidity":64.00, "co2":1241.00},
    {"temperature":31.00, "humidity":64.00, "co2":1241.00},
    {"temperature":31.00, "humidity":78.00, "co2":1241.00},
    {"temperature":31.00, "humidity":97.50, "co2":1241.00},
    {"temperature":31.00, "humidity":97.50, "co2":1241.00},
    {"temperature":50.40, "humidity":86.50, "co2":1241.00},
    {"temperature":50.40, "humidity":86.50, "co2":1241.00},
    {"temperature":50.40, "humidity":86.50, "co2":1241.00},
    {"temperature":50.40, "humidity":86.50, "co2":1241.00}
]

conn = mysql.connector.connect(
    host="localhost",
    user="climate_user",
    password="climate_pass",
    database="climate_db"
)

cursor = conn.cursor()

for entry in dataset:
    cursor.execute(
        "INSERT INTO climate_logs (temperature, humidity, co2) VALUES (%s, %s, %s)",
        (entry["temperature"], entry["humidity"], entry["co2"])
    )

conn.commit()
cursor.close()
conn.close()
print("Data inserted successfully!")
