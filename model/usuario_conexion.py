import mysql.connector

class UsuarioConexion:
    def __init__(self):
        self.conexion = None
        self.conectar()

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                port='3306',
                user='root',
                password='',
                database='bcs_claro'
            )
            if self.conexion.is_connected():
                print("Conexión a la base de datos exitosa.")
        except mysql.connector.Error as err:
            print(f"Error de base de datos: {err}")
        finally:
            if self.conexion and not self.conexion.is_connected():
                self.conexion.close()

    def read_client_authentication(self, username: str, password: str, grant_type: str, client_id: str, client_secret: str):
        try:
            cursor = self.conexion.cursor()
            query = """SELECT * FROM authentication 
                       WHERE username = %s AND password = %s 
                       AND grant_type = %s AND client_id = %s 
                       AND client_secret = %s"""
            cursor.execute(query, (username, password, grant_type, client_id, client_secret))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"ERROR al seleccionar partner_code: {err}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update_or_insert_token(self, username: str, token: str):
        try:
            if self.read_username(username):
                cursor = self.conexion.cursor()
                query_update = "UPDATE users SET token = %s WHERE username = %s"
                cursor.execute(query_update, (token, username))
                self.conexion.commit()
                print(f"Token actualizado para username: {username}")
            else:
                print(f"No se encontró el username: {username}")
        except mysql.connector.Error as err:
            print(f"ERROR al actualizar el token: {err}")
        finally:
            if cursor:
                cursor.close()

    def read_username(self, username: str):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT username FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"ERROR al seleccionar username: {err}")
            return None
        finally:
            if cursor:
                cursor.close()            

    def read_validate_users(self, partner_code: str, Authorization: str, Username: str, password: str):
        try:
            cursor = self.conexion.cursor()
            query = """SELECT * FROM users 
                    WHERE partner_code = %s AND token = %s 
                    AND username = %s 
                    AND password = %s"""
            cursor.execute(query, (partner_code, Authorization, Username, password))
            result = cursor.fetchone()
            return result if result else None
        except mysql.connector.Error as err:
            print(f"ERROR al seleccionar partner_code: {err}")
            return None
        finally:
            if cursor:
                cursor.close()

    def read_score_client(self, authtoken: str, phone_no: str):
        try:
            cursor = self.conexion.cursor()
            query = "SELECT credit_score FROM users WHERE token = %s AND phone_no = %s"
            cursor.execute(query, (authtoken, phone_no))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"ERROR al seleccionar username: {err}")
            return None
        finally:
            if cursor:
                cursor.close() 

    def read_logout_users(self, partner_code: str, username: str):
        try:
            with self.conexion.cursor() as cursor:
                query = """SELECT * FROM users 
                        WHERE partner_code = %s AND username = %s 
                        LIMIT 1"""
                cursor.execute(query, (partner_code, username))
                result = cursor.fetchone()
                return result if result else None
        except mysql.connector.Error as err:
            print(f"ERROR al seleccionar partner_code: {err}")
            return None            



        
