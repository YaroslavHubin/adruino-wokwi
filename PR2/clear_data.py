import mysql.connector

def clear_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="climate_user",
        password="climate_pass",
        database="climate_db"
    )
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE climate_logs;")
    conn.commit()
    cursor.close()
    conn.close()
    print("База даних очищена: всі записи видалені.")

if __name__ == "__main__":
    clear_database()
