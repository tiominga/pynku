from django.shortcuts import render
from connection.models import Connection 
import MySQLdb


def editor_connection(request):
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
            cursor = connection.cursor()
            return cursor
        except MySQLdb.Error as e:
            print(f"Error connecting to MySQL: {e}")
    return None


def editor_index(request):
    print("ID da conexão:", request.session.get('id_connection'))
    arr_tables = []  
    cursor = editor_connection(request)
   
    if cursor:
        try:
            cursor.execute("SHOW TABLES")
            arr_tables = cursor.fetchall()
            for table in arr_tables:
                print(table[0])
        except MySQLdb.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()

    return render(request, 'editor/editor.html', {'arr_tables': arr_tables})
