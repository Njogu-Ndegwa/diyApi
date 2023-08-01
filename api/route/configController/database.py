import mysql.connector

class MySQLConnection:
    """
    Connect to MySQL database and perform queries
    ------
    
    Attributes
    ----------
    host : str
        MySQL database hostname
    user : str
        Name of MySQL database user
    password : str
        Password to access the MySQL database 
    database : str
        Name of the MySQL database to connect to
    
    Methods
    -------
    close()
        Closes the MySQL database connection
    query()
        Performs input SQL query and returns data   
    """
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            print("Failed to connect to MySQL database:", e)
        
    def close(self):
        if self.connection is not None:
            self.connection.close()
        
    def query(self, query, data=None):
        assert self.connection is not None, "MySQL connection not initialized!"
        cursor = None
        response = None
        try:
            cursor = self.connection.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            response = cursor.fetchall()
            self.connection.commit()
        except Exception as e:
            print("MySQL query failed:", e)
        finally:
            if cursor is not None:
                cursor.close()
        return response
