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

    # 1) Try to connect 2)Run Docker 3)Wait 4)Try connecting again
    def start_docker_and_connect_db(self) -> bool:
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
            print("Please Start Docker App First")
            return False

        max = 20
        for i in range(max):
            try:
                self.conn = psycopg2.connect(**self.conn_params)
                self.cursor = self.conn.cursor()
                print("✅ Docker and Database successfully started and ready!")
                return True
            except psycopg2.OperationalError:
                print(f"⏳ Waiting for database to wake up... ({i+1}/{max})")
                time.sleep(1)

    # Login Check
    def check_login(self, username, password) -> int:
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()            
            if user:
                return 1    
            else: 
                return 0
                
        except Exception as e:
            self.conn.rollback()
            return f"Error: {str(e)}"
        
    def save_log(self,username : str, new_log : list) -> str: 
        date = new_log[0]
        operation = new_log[0]
        variables = new_log[0]
        input_data = new_log[0]
        output = new_log[0]
        chart = new_log[0]

        try:
            query = """
                    INSERT INTO history (user_id,date,operation,variables,input_data,output,chart)
                    VALUES (
                            (SELECT id FROM users WHERE username = %s), %s, %s, %s, %s, %s, %s
                    ) RETURNING id;
                    """
            self.cursor.execute(query, (username,date,operation,variables,input_data,output,chart))

            self.conn.commit()
            db_id = self.cursor.fetchone()

            if db_id:
                return db_id[0]
            else:
                return None
            
        except Exception as e:
            self.conn.rollback()
            print(str(e))
            return f"Error : {str(e)}"
            
        
    def return_logs_by_date(self,username,log_date) -> list:
        try:
            query = """
                    SELECT (id,date,operation,variables) FROM history
                    WHERE user_id = (SELECT id FROM users WHERE username = %s)
                    AND date::date BETWEEN %s AND %s ORDER BY date DESC
                    """
            self.cursor.execute(query,(username,log_date[0],log_date[1]))
            log_by_date_data = self.cursor.fetchall()
            return log_by_date_data
        
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"
        
    def return_log_by_id(self,db_id : str) -> list:
        try:
            query = """
                    SELECT * FROM history WHERE id = %s
                    """
            self.cursor.execute(query,(db_id))
            log_by_id_data = self.cursor.fetchall()
            return log_by_id_data
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"

    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()    


