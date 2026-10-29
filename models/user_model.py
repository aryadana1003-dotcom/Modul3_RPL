# Aryadana Agung Karama F5212510013
import hashlib
from config.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # plain text diubah ke sha-256
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def autentikasi(self, username, password):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)
            # Parameterized Query untuk mencegah SQL Injection
            query = "SELECT id_user, username, role FROM " + self.table_name + " WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user
        return None

    def register_user(self, username, password, role):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                # Enkripsi password sebelum disimpan
                password_hash = self.hash_password(password)
                query = "INSERT INTO " + self.table_name + " (username, password, role) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, password_hash, role))
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Error saat registrasi: {e}")
                return False
        return False
