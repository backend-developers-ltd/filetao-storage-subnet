import sqlite3

sqlite = None

def get_sqlite():
    global sqlite
    if not sqlite:
        sqlite = sqlite3.connect("network_data.db")
    return sqlite

def query(query, params):
    sqlite = get_sqlite()
    try:
        with sqlite.cursor() as cursor:
            # Execute the SQL command
            cursor.execute(query, params)
            
            # Fetch the results
            results = cursor.fetchall()
            
            # If you want to print the results:
            for row in results:
                print(row)
            
            # Or if you prefer to return the results for further processing:
            return results
            
    except sqlite3.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")