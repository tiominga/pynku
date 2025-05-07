import MySQLdb
from connection.models import Connection

def get_connection(request):
    id_connection = request.session.get('id_connection')   
    obj_connection = Connection.objects.filter(id=id_connection).first()

    if obj_connection:
        try:
            connection = MySQLdb.connect(
                host=obj_connection.host,
                port=obj_connection.port,
                user=obj_connection.user,
                passwd=obj_connection.password,
                db=obj_connection.database
            )
            connection.autocommit(True)
            cursor = connection.cursor()
            return cursor
        except MySQLdb.Error as e:
            print(f"Error connecting to MySQL: {e}")
    return None