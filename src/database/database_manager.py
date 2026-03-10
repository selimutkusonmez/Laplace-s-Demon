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
        
    # NewOperationUI.calculation_success --> AppManager --> DatabaseManager.save_log --> AppManager --> LogsUI.add_new_log
    def save_log(self,username : str, new_log : list) -> str:
        date = new_log[0]
        operation = new_log[1]
        variables = new_log[2]
        input_data = new_log[3]
        output = new_log[4]

        try:
            query = """
                    INSERT INTO history (user_id,date,operation,variables,input_data,output)
                    VALUES (
                            (SELECT id FROM users WHERE username = %s), %s, %s, %s, %s, %s
                    ) RETURNING id;
                    """
            self.cursor.execute(query, (username,date,operation,variables,input_data,output))

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
            
    # LogsUI.logs_button_function.logs_by_date_requested --> AppManager --> DatabaseManager.return_logs_by_date --> AppManager --> LogsUI.show_logs_by_date
    def return_logs_by_date(self,username,log_date) -> list:
        try:
            query = """
                    SELECT id,date,operation,variables FROM history
                    WHERE user_id = (SELECT id FROM users WHERE username = %s)
                    AND date::date BETWEEN %s AND %s ORDER BY date DESC
                    """
            self.cursor.execute(query,(username,log_date[0],log_date[1]))
            log_by_date_data = self.cursor.fetchall()
            return log_by_date_data
        
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"
        

    #LogsUI.show_log_by_id.log_by_id_requested --> AppManager --> DatabaseManager_return_log_by_id --> AppManager --> LogsUI.init_history_ui    
    def return_log_by_id(self,db_id : str) -> list:
        try:
            query = """
                    SELECT * FROM history WHERE id = %s
                    """
            self.cursor.execute(query,(db_id,))
            log_by_id_data = self.cursor.fetchall()
            print(log_by_id_data[0])
            return log_by_id_data[0]
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"

    def count_logs(self,username):
        try:
            query = """
            SELECT COUNT(user_id) FROM history
            WHERE user_id = (SELECT id FROM users WHERE username = %s)
            """
            self.cursor.execute(query, (username,))
            total_count = self.cursor.fetchone()[0]
            return total_count
        except Exception as e:
            print(str(e))


    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()    


