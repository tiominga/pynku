from django.shortcuts import render
from connection.models import Connection 
import MySQLdb
from django.http import JsonResponse
import json
from pynku.utils.sql_to_table import SqlToTable
from pynku.utils.db_connection import get_connection




def get_table(request):

    obj_sql_to_table = SqlToTable()
    obj_sql_to_table.set_query(request.POST.get("query"))

    obj_sql_to_table.set_params(None)  # Se necessário, adicione os parâmetros

    html_table = obj_sql_to_table.query_to_html(request)    
    return JsonResponse({"html": html_table})

def get_database_name(request):
    id_connection = request.session.get('id_connection')   
    obj_connection = Connection.objects.filter(id=id_connection).first()
    database_name = obj_connection.database
    return database_name



def editor_index(request):    
    arr_tables = []  
    cursor = get_connection(request)
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
