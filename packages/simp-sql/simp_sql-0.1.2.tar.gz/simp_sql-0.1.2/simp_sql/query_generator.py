class QueryGenerator:
    def __init__(self, cursor):
        self.cursor = cursor

    def select_query(self, columns, table, where=None):
        """Generate and execute a SELECT query with optional WHERE clause."""
        # If no columns specified, select all columns from the table
        if columns:
            query = f"SELECT {', '.join(columns)} FROM {table}"
        else:
            query = f"SELECT * FROM {table}"

        if where:
            query += f" WHERE {where}"
        
        return self.execute_query(query)

    def join(self, table1, table2, join_type="INNER", on=None, where=None):
        """Generate a JOIN query with optional WHERE clause."""
        # Construct the JOIN query based on provided parameters
        if on:
            query = f"SELECT * FROM {table1} {join_type} JOIN {table2} ON {on}"
        else:
            query = f"SELECT * FROM {table1} {join_type} JOIN {table2}"
        
        if where:
            query += f" WHERE {where}"

        return self.execute_query(query)

    def aggregate(self, table, groupby, aggre, aggrecol):
        """Generate and execute an aggregate query."""
        # Create a string of aggregated columns if aggrecol is provided
        if aggrecol:
            columns = ', '.join([f"{aggre}({col})" for col in aggrecol])
            query = f"SELECT {aggrecol},{columns} FROM {table} GROUP BY {groupby}"
        else:
            query = f"SELECT {aggrecol},{aggre}(*) FROM {table} GROUP BY {groupby}"
    
        return self.execute_query(query)

    def delete_query(self, table, where):
        """Generate and execute a DELETE query."""
        query = f"DELETE FROM {table} WHERE {where}"
        try:
            self.cursor.execute(query)
            return self.cursor.rowcount  # Return the number of deleted rows
        except Exception as e:
            print(f"Error executing delete query: {e}")
            return None
    def execute_query(self, query):
        """Execute the given SQL query and return the results."""
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()  # Fetch all results from the executed query
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
