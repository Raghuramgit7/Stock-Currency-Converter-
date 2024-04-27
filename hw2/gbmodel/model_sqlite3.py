from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(name) from guestbook1")
        except sqlite3.OperationalError:
            cursor.execute("create table guestbook1 (id, quote, name, dateofquote, sourcetype, sourcequote, rating)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, email, date, message
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM guestbook1")
        return cursor.fetchall()
    
    
    def insert(self, id, quote, name, dateofquote, sourcetype, sourcequote, rating):
        """
        Inserts entry into database
        :param quote: String
        :param name: String
        :param dateofquote: date
        :param sourcetype: String
        :param sourcequote: String
        :param rating: Integer
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'id': id, 'quote': quote, 'name': name, 'dateofquote': dateofquote, 'sourcetype': sourcetype, 'sourcequote': sourcequote, 'rating': rating}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into guestbook1 (id, quote, name, dateofquote, sourcetype, sourcequote, rating) VALUES (:id, :quote, :name, :dateofquote, :sourcetype, :sourcequote, :rating)", params)

        connection.commit()
        cursor.close()
        return True
    
    

    
        
        
