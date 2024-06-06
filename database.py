import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        user="ganesh",
        password="microsoft@123",
        host="loginfrt-mysql-server123.mysql.database.azure.com",
        port=3306,
        database="your_database_name",
        ssl_ca=r'C:\Certificates\DigiCertGlobalRootG2.crt.pem',
        ssl_disabled=False
    )

def load_jobs_from_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        return jobs
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def load_job_from_db(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE id = %s", (id,))
        row = cursor.fetchone()
        return row if row else None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def add_application_to_db(job_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (
            job_id,
            data['full_name'],
            data['email'],
            data['linkedin_url'],
            data['education'],
            data['work_experience'],
            data['resume_url']
        ))
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
