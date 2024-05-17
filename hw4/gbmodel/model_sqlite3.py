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
    
    def delete(self, id):
        # Delete a specific record from the 'quotes' table based on 'rowid'
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM guestbook1 WHERE id=?", (id,))
        connection.commit()
        cursor.close()
        return True
    
    def update(self, updated_entry):
        # Update a specific record in the 'quotes' table based on 'id'
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        
        id_value = updated_entry.get('id')
        if id_value is None:
            # If 'id' is not provided in 'updated_entry', return False indicating failure
            return False
        
        # Build  SQL query to update the record
        params = {'id': id_value, 'quote': updated_entry.get('quote'), 'name': updated_entry.get('name'), 'dateofquote': updated_entry.get('dateofquote'), 'sourcetype': updated_entry.get('sourcetype'), 'sourcequote': updated_entry.get('sourcequote'), 'rating': updated_entry.get('rating')}

        
        # Execute the update query with the updated_entry dictionary
        
        cursor.execute(
            "UPDATE guestbook1 SET quote = :quote, name = :name, dateofquote = :dateofquote, sourcetype = :sourcetype, sourcequote = :sourcequote, rating = :rating WHERE id=:id",
            params,
        )
        
        connection.commit()
        cursor.close()
        
        return True
    
    def get(self, id):
        """
        Gets a specific row from the database based on the provided id.
        Returns the row if found, otherwise returns None.
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM guestbook1 WHERE id=?", (id,))
        row = cursor.fetchone()  # Fetch the first row
        connection.close()  # Close connection after fetching

        return row
    

    
        
        
