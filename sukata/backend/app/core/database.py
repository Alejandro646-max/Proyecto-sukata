import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Conexión a MySQL"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password='Adm*2025',  # Tu contraseña directa
                database=os.getenv('DB_NAME', 'sukata_db')
            )
            print("✅ Conectado a MySQL")
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            self.connection = None
    
    def execute_query(self, query, params=None):
        """Ejecutar INSERT, UPDATE, DELETE"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self._connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def fetch_all(self, query, params=None):
        """Obtener todos los registros"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self._connect()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def fetch_one(self, query, params=None):
        """Obtener un registro"""
        results = self.fetch_all(query, params)
        return results[0] if results else None

db = Database()