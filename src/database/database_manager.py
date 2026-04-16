import psycopg2
from getmac import get_mac_address
import subprocess
import time
import socket
import secrets
from src.logic.hash_password.hash_password import hash_password,verify_password

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

    #AppManager --> AppManager.init_database_manager --> DatabaseManager.start_docker_and_connect_db
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


    #                   LOGIN AND LOGS (users and logs tables)

    #LoginUI.login_button_function.login_requested --> AppManager.handle_login --> DatabaseManager.check_login --> DatabaseManager.save_user_log
    def save_user_log(self,username : str, attempt : str) -> None:
        try:
            mac_adress = get_mac_address()
            hostname = socket.gethostname()
            ip_adress = socket.gethostbyname(hostname)
        
        except:
            mac_adress = "Offline"
            hostname = "Offline"
            ip_adress = "Offline"
        try:
            query = """
                    INSERT INTO logs (user_id,ip_adress,mac_adress,attempt)
                    VALUES (
                            (SELECT id FROM users WHERE username = %s), %s, %s, %s
                    )
                    """
            self.cursor.execute(query,(username,ip_adress,mac_adress,attempt))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()

    #LoginUI.login_button_function.login_requested --> AppManager.handle_login --> DatabaseManager.check_login.login_code --> AppManager.handle_login
    def check_login(self, username : str, plain_text_password : str):
        try:
            query = "SELECT password FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()    
            
            if result is None:
                self.conn.rollback()
                return False, None
            
            stored_hash = result[0]
            if verify_password(plain_text_password,stored_hash):
                auth_token = secrets.token_hex(32) 

                update_query  = "UPDATE users SET auth_token = %s WHERE username = %s"
                self.cursor.execute(update_query, (auth_token,username))
                self.conn.commit()      

                self.save_user_log(username,"successful")

                return True , auth_token    
            else: 
                self.save_user_log(username,"failed")
                return False, None
                
        except Exception as e:
            self.conn.rollback()
            return f"Error: {str(e)}"
        
    # AppManager.init_main_ui --> DatabaseManager.check_token_login
    def check_token_login(self, username: str, auth_token: str) -> bool:
        try:
            query = "SELECT auth_token FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()    
            
            # If the database token matches the local registry token exactly
            if result is not None and result[0] == auth_token:
                self.save_user_log(username, "silent_token_success")
                return True
            else:
                return False
                
        except Exception as e:
            self.conn.rollback()
            return False
        
    #AppManager.handle_relogin --> DatabaseManager.revoke_token
    def revoke_token(self, username: str) -> None:
        try:
            query = "UPDATE users SET auth_token = NULL WHERE username = %s"
            self.cursor.execute(query, (username,))
            self.conn.commit()

        except Exception as e:
            self.conn.rollback()


    #                   CREATE NEW ACCOUNT (users)

    # CreateNewAccountUI.create_my_account_button_function.save_account_info_requested --> AppManager.handle_create_new_account --> AppManager.handle_save_account_info --> DatabaseManager.save_account_info
    def save_account_info(self,account_info : list) -> str:
        try:
            username = account_info[0]
            raw_password = account_info[1]

            secure_hash = hash_password(raw_password)

            query = """
                    INSERT INTO users (username,password) VALUES (%s,%s)
                    """
            self.cursor.execute(query, (username,secure_hash))

            self.conn.commit()

            return "Account Created Successfully"
            
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            return "Username Already In Use"
            
        except psycopg2.Error:
            self.conn.rollback()
            return "An Error Occured With Database"
            
        except Exception:
            self.conn.rollback()
            return "An Error Occured With System"


    #                   SAVE OPERATION DATA -- GET OPERATION DATA BY ID OR DATE -- COUNT TOTAL OPERATION BASED ON user_id (operation_history table)

    # NewOperationUI.calculation_success --> AppManager.handle_new_archive_record --> DatabaseManager.save_archive_record
    def save_archive_record(self, username : str, new_log : list) -> str:
        date = new_log[0]
        operation = new_log[1]
        variables = new_log[2]
        input_data = new_log[3]
        output = new_log[4]

        try:
            query = """
                    INSERT INTO operation_history (user_id,date,operation,variables,input_data,output)
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
            
    # LaplaceArchiveUI.list_archive_records_by_date_button_function.archive_records_by_date_requested --> AppManager.hanlde_archive_records_by_date --> DatabaseManager.return_logs_by_date list_archive_records_by_date
    def return_archive_records_by_date(self, username : str,records_start_end_date : str) -> list:
        try:
            query = """
                    SELECT id,date,operation,variables FROM operation_history
                    WHERE user_id = (SELECT id FROM users WHERE username = %s)
                    AND date::date BETWEEN %s AND %s ORDER BY date DESC
                    """
            self.cursor.execute(query,(username,records_start_end_date[0],records_start_end_date[1]))
            log_by_date_data = self.cursor.fetchall()
            return log_by_date_data
        
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"
        
    # LaplaceArchiveUI.request_archive_record_data_by_id.archive_record_data_by_id_requested --> AppManager.handle_archive_record_data_by_id --> DatabaseManager_return_operation_data_by_id
    def return_archive_record_data_by_id(self, db_id : str) -> list:
        try:
            query = """
                    SELECT * FROM operation_history WHERE id = %s
                    """
            self.cursor.execute(query,(db_id,))
            log_by_id_data = self.cursor.fetchall()
            print(log_by_id_data)
            print(type(log_by_id_data))
            return log_by_id_data[0]
        except Exception as e:
            print(str(e))
            return f"Error : {str(e)}"

    #DatabaseManager.count_archive_records_on_id --> AppManager.handle_login --> OperationHistoryUI(self.operation_data_count)
    def count_archive_records_on_id(self, username : str) -> str:
        try:
            query = """
            SELECT COUNT(user_id) FROM operation_history
            WHERE user_id = (SELECT id FROM users WHERE username = %s)
            """
            self.cursor.execute(query, (username,))
            total_count = self.cursor.fetchone()[0]
            return total_count
        
        except Exception as e:
            print(str(e))


    #                   USER PREFERENCES (user_preferences table)

    def pull_user_preferences(self,username : str) -> list:
        try:
            query = """
                    SELECT * FROM user_preferences WHERE user_id = (SELECT id FROM users WHERE username = %s)
                    """
            self.cursor.execute(query,(username,))
            current_user_preferences = self.cursor.fetchone()
            return current_user_preferences

        except:
            self.conn.rollback()
        
    def pull_user_stats(self,username : str) -> list:
        try:
            query = "SELECT * FROM user_stats WHERE user_id = (SELECT id FROM users WHERE username = %s)"
            self.cursor.execute(query,(username,))
            return self.cursor.fetchone()
        except:
            self.conn.rollback()

    #PreferencesUI.save_preferred_language.change_preferred_language_request --> AppManager.handle_preferred_language_change --> DatabaseManager.update_preferred_language
    def update_preferred_language(self, username : str, preferred_language : str) -> None:
        try:
            query = """
                    UPDATE user_preferences SET preferred_language = %s WHERE user_id = (SELECT id FROM users WHERE username = %s);
                    """
            self.cursor.execute(query,(preferred_language,username))
            self.conn.commit()
            print("language db")
            
        except Exception as e:
            print(str(e))
            self.conn.rollback()

    #PreferencesUI.save_preferred_theme.change_preferred_theme_request --> AppManager.handle_preferred_theme_change --> DatabaseManager.update_preferred_theme
    def update_preferred_theme(self, username : str, preferred_theme : str) -> None :
        try:
            query = """
                    UPDATE user_preferences SET preferred_theme = %s WHERE user_id = (SELECT id FROM users WHERE username = %s);
                    """
            self.cursor.execute(query,(preferred_theme,username))
            self.conn.commit()
            print("theme db")
        except:
            self.conn.rollback()

    #PreferencesUI.save_preferred_font_color.change_preferred_font_color_request --> AppManager.handle_preffered_font_color_change --> DatabaseManager.update_preferred_font_color
    def update_preferred_font_color(self, username : str, preferred_font_color : str) -> None:
        try:
            query = """
                    UPDATE user_preferences SET preferred_font_color = %s WHERE user_id = (SELECT id FROM users WHERE username = %s);
                    """
            self.cursor.execute(query,(preferred_font_color,username))
            self.conn.commit()
        except:
            self.conn.rollback()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()    


