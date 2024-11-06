class QueryGenerator:
    def __init__(self, cursor):
        self.cursor = cursor

    def select_query(self, columns, table, where=None, groupby=None, aggre=None, aggrecol=None):

        if aggre and aggrecol:
            # Aggregate columns if specified
            aggre_columns = ', '.join([f"{aggre}({col})" for col in aggrecol])
            select_clause = f"{groupby}, {aggre_columns}" if groupby else aggre_columns
        else:
            # Use specified columns or select all
            select_clause = ', '.join(columns) if columns else '*'
        
        query = f"SELECT {select_clause} FROM {table}"

        if where:
            query += f" WHERE {where}"
        if groupby:
            query += f" GROUP BY {groupby}"
        
        return self.execute_query(query)

    def join(self, table1, table2, join_type="INNER", on=None, where=None):

        if on:
            query = f"SELECT * FROM {table1} {join_type} JOIN {table2} ON {on}"
        else:
            query = f"SELECT * FROM {table1} {join_type} JOIN {table2}"
        
        if where:
            query += f" WHERE {where}"
        
        return self.execute_query(query)

    def delete_query(self, table, where):

        query = f"DELETE FROM {table} WHERE {where}"
        try:
            self.cursor.execute(query)
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error executing delete query: {e}")
            return None

    def execute_query(self, query):

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
