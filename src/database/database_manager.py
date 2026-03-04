import psycopg2
import datetime
import subprocess
import time

class DatabaseManager():
    def __init__(self):
        self.conn_params = {
            "host": "127.0.0.1",
            "port": "5432",
            "database": "laplace_db",
            "user": "admin",
            "password": "1234",
            "connect_timeout": 2
        }
        self.start_docker_and_connect_db()

    def start_docker_and_connect_db(self):
        print("Checking system status...")
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor()
            print("✅ Database is already running! Skipping Docker command.")
            return True
        except psycopg2.OperationalError:
            print("⚠️ Database is down. Starting Docker...")

        try:
            subprocess.run(["docker-compose","up","-d"],check=True)
        except Exception as e:
            print(f"❌ Critical Error: Failed to execute Docker command! Error: {e}")
            return False

        max = 10
        for i in range(max):
            try:
                self.conn = psycopg2.connect(**self.conn_params)
                self.cursor = self.conn.cursor()
                print("✅ Docker and Database successfully started and ready!")
                return True
            except psycopg2.OperationalError:
                print(f"⏳ Waiting for database to wake up... ({i+1}/{max})")
                time.sleep(1)


