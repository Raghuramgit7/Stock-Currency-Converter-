class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, id, quote, name, dateofquote, sourcetype, sourcequote, rating):
        """
        Inserts entry into database
        :param quote: String
        :param name: String
        :param dateofquote: date
        :param sourcetype: String
        :param sourcequote: String
        :param rating: Integer
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass

   