import mysql.connector
from mysql.connector import Error
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    A class to handle MySQL database connections and operations.
    """
    
    def __init__(self, config_file=None, host=None, database=None, user=None, password=None):
        """
        Initialize database connection parameters either from a config file or direct parameters.
        
        Args:
            config_file (str): Path to the database configuration file (JSON format)
            host (str): Database host
            database (str): Database name
            user (str): Database username
            password (str): Database password
        """
        self.connection = None
        self.cursor = None
        
        # If config file is provided, load parameters from it
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.host = config.get('host')
                    self.database = config.get('database')
                    self.user = config.get('user')
                    self.password = config.get('password')
                    logger.info(f"Loaded database configuration from {config_file}")
            except Exception as e:
                logger.error(f"Error loading config file: {str(e)}")
                raise
        # Otherwise use the provided parameters
        else:
            self.host = host
            self.database = database
            self.user = user
            self.password = password
    
    def connect(self):
        """
        Establish a connection to the MySQL database.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logger.info(f"Connected to MySQL Server version {db_info}")
                self.cursor = self.connection.cursor(dictionary=True)
                self.cursor.execute("SELECT DATABASE();")
                record = self.cursor.fetchone()
                logger.info(f"Connected to database: {record['DATABASE()']}") 
                return True
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {str(e)}")
            return False
    
    def disconnect(self):
        """
        Close the database connection.
        """
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            logger.info("MySQL connection closed")
    
    def execute_query(self, query, params=None, commit=False):
        """
        Execute a SQL query.
        
        Args:
            query (str): SQL query to execute
            params (tuple, dict, list): Parameters for the query
            commit (bool): Whether to commit the transaction
            
        Returns:
            list: Query results if applicable, None otherwise
        """
        try:
            if not self.connection or not self.connection.is_connected():
                logger.warning("No active connection. Attempting to reconnect...")
                self.connect()
            
            self.cursor.execute(query, params)
            
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                result = self.cursor.fetchall()
                logger.info(f"Query executed successfully. Returned {len(result)} rows.")
                return result
            
            if commit:
                self.connection.commit()
                logger.info(f"Query executed successfully. Rows affected: {self.cursor.rowcount}")
            
            return None
        except Error as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query}")
            if params:
                logger.error(f"Parameters: {params}")
            raise
    
    def execute_many(self, query, params_list, commit=True):
        """
        Execute a SQL query with multiple parameter sets.
        
        Args:
            query (str): SQL query to execute
            params_list (list): List of parameter sets
            commit (bool): Whether to commit the transaction
            
        Returns:
            int: Number of rows affected
        """
        try:
            if not self.connection or not self.connection.is_connected():
                logger.warning("No active connection. Attempting to reconnect...")
                self.connect()
            
            self.cursor.executemany(query, params_list)
            
            if commit:
                self.connection.commit()
                logger.info(f"Query executed successfully. Rows affected: {self.cursor.rowcount}")
            
            return self.cursor.rowcount
        except Error as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Parameters: {params_list}")
            raise
    
    def call_procedure(self, procedure_name, params=None, commit=False):
        """
        Call a stored procedure.
        
        Args:
            procedure_name (str): Name of the stored procedure
            params (tuple): Parameters for the stored procedure
            commit (bool): Whether to commit the transaction
            
        Returns:
            list: Results from the stored procedure if applicable, None otherwise
        """
        try:
            if not self.connection or not self.connection.is_connected():
                logger.warning("No active connection. Attempting to reconnect...")
                self.connect()
            
            self.cursor.callproc(procedure_name, params)
            
            # Get results if any
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            
            if commit:
                self.connection.commit()
                logger.info(f"Stored procedure {procedure_name} executed successfully.")
            
            return results if results else None
        except Error as e:
            logger.error(f"Error calling stored procedure: {str(e)}")
            logger.error(f"Procedure: {procedure_name}")
            if params:
                logger.error(f"Parameters: {params}")
            raise
    
    def create_table(self, table_name, columns):
        """
        Create a new table.
        
        Args:
            table_name (str): Name of the table to create
            columns (list): List of column definitions
            
        Returns:
            bool: True if table was created successfully, False otherwise
        """
        try:
            # Check if table already exists
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if self.cursor.fetchone():
                logger.warning(f"Table {table_name} already exists")
                return False
            
            # Create table
            query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
            self.cursor.execute(query)
            self.connection.commit()
            logger.info(f"Table {table_name} created successfully")
            return True
        except Error as e:
            logger.error(f"Error creating table: {str(e)}")
            return False
    
    def drop_table(self, table_name):
        """
        Drop a table.
        
        Args:
            table_name (str): Name of the table to drop
            
        Returns:
            bool: True if table was dropped successfully, False otherwise
        """
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(query)
            self.connection.commit()
            logger.info(f"Table {table_name} dropped successfully")
            return True
        except Error as e:
            logger.error(f"Error dropping table: {str(e)}")
            return False
    
    def insert_data(self, table_name, data):
        """
        Insert data into a table.
        
        Args:
            table_name (str): Name of the table
            data (dict): Dictionary with column names as keys and values to insert
            
        Returns:
            int: ID of the inserted row if available, None otherwise
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            
            logger.info(f"Data inserted successfully into {table_name}")
            return self.cursor.lastrowid
        except Error as e:
            logger.error(f"Error inserting data: {str(e)}")
            return None
    
    def update_data(self, table_name, data, condition):
        """
        Update data in a table.
        
        Args:
            table_name (str): Name of the table
            data (dict): Dictionary with column names as keys and new values
            condition (str): WHERE condition for the update
            
        Returns:
            int: Number of rows affected
        """
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            
            logger.info(f"Data updated successfully in {table_name}. Rows affected: {self.cursor.rowcount}")
            return self.cursor.rowcount
        except Error as e:
            logger.error(f"Error updating data: {str(e)}")
            return 0
    
    def delete_data(self, table_name, condition):
        """
        Delete data from a table.
        
        Args:
            table_name (str): Name of the table
            condition (str): WHERE condition for the delete
            
        Returns:
            int: Number of rows affected
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            
            self.cursor.execute(query)
            self.connection.commit()
            
            logger.info(f"Data deleted successfully from {table_name}. Rows affected: {self.cursor.rowcount}")
            return self.cursor.rowcount
        except Error as e:
            logger.error(f"Error deleting data: {str(e)}")
            return 0
    
    def truncate_table(self, table_name):
        """
        Truncate a table (remove all rows).
        
        Args:
            table_name (str): Name of the table to truncate
            
        Returns:
            bool: True if table was truncated successfully, False otherwise
        """
        try:
            query = f"TRUNCATE TABLE {table_name}"
            self.cursor.execute(query)
            self.connection.commit()
            logger.info(f"Table {table_name} truncated successfully")
            return True
        except Error as e:
            logger.error(f"Error truncating table: {str(e)}")
            return False
