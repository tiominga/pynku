import MySQLdb
MySQLError = MySQLdb.MySQLError  # Explicitly access MySQLError from MySQLdb
from connection.models import Connection

def get_connection(request):
    # Retrieve the connection ID from the session
    id_connection = request.session.get('id_connection')
    
    # Fetch the connection object from the database
    obj_connection = Connection.objects.filter(id=id_connection).first()

    if obj_connection:
        try:
            # Attempt to establish a connection to the MySQL database
            connection = MySQLdb.connect(
                host=obj_connection.host,
                port=obj_connection.port,
                user=obj_connection.user,
                passwd=obj_connection.password,
                db=obj_connection.database,
                charset='utf8mb4',  # Set charset to UTF-8
            )
            connection.autocommit(True)
            cursor = connection.cursor()
            return cursor
        except MySQLError as e:
            # In case of an error, print the error message
            print(f"Error connecting to MySQL: {e}")
        finally:
            # Ensure the connection is closed in case of an error (optional, but useful)
            if connection:
                connection.close()
    else:
        print("Could not find the connection object in the database.")
    
    # If no connection or error occurs, return None
    return None
