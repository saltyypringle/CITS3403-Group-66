import sqlite3
import os 
from flask_login import UserMixin

#Function that opens the database
def connect_db():
    path_way_to_db = os.path.join(os.path.dirname(__file__), 'data', 'sukiscan.db')
    return sqlite3.connect(path_way_to_db)

#Gets Account Information from Database
class AccountInfo(UserMixin):
    def __init__(self, id, email, username, password):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
    
    #Function for Account Information
    @staticmethod
    def Get_Info(e_u):
        #Connect to the Database
        conn = connect_db()
        cursor = conn.cursor()
        
        #Query to get information for email and username
        query = "SELECT * FROM User WHERE email = ? OR username = ?"
        cursor.execute(query, (e_u, e_u))
        data = cursor.fetchone()
        conn.close()
        
        if data:
            return AccountInfo(*data)
        return None
    