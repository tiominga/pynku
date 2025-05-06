from django.shortcuts import render
from connection.models import Connection 
import MySQLdb
from django.http import JsonResponse
import json
from pynku.utils.sql_to_table import SqlToTable


def get_table(request):
    # Captura a query do POST
    query = request.POST.get('query')
    print(query)
    
    # Cria o objeto SqlToTable e passa a query
    obj_sql_to_table = SqlToTable()
    obj_sql_to_table.set_query(query)
    
    # A seguir, suponha que obj_sql_to_table.get_table() retorne uma tabela HTML
    html_table = obj_sql_to_table.query_to_html()

    # Retorna a tabela HTML como resposta (poderia retornar JSON, mas aqui estamos retornando HTML diretamente)
    return JsonResponse({'table_html': html_table})

def get_database_name(request):
    id_connection = request.session.get('id_connection')   
    obj_connection = Connection.objects.filter(id=id_connection).first()
    database_name = obj_connection.database
    return database_name

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
    database_name = get_database_name(request)
   
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

    return render(request, 'editor/editor.html', {
        'arr_tables': arr_tables,
        'database_name': database_name,
        })
