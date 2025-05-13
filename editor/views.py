from django.shortcuts import render
from connection.models import Connection 
import MySQLdb
from django.http import JsonResponse
from django.http import HttpResponse
import json
from pynku.utils.sql_to_table import SqlToTable
from pynku.utils.db_connection import get_connection
import re


def get_table(request):
    obj_sql_to_table = SqlToTable()
    obj_sql_to_table.set_query(request.POST.get("query"))
    obj_sql_to_table.set_params(None) 
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
           
        except MySQLdb.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()

    return render(request, 'editor/editor.html', {
        'arr_tables': arr_tables,
        'database_name': database_name,
        })

def query_to_json(request,query):
    cursor = get_connection(request)
    
    if cursor:
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            return result
        except MySQLdb.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()

   
    
def get_model(request):
    table_name = request.POST.get("table_name")   
    query = f"describe {table_name}"           
    json = query_to_json(request,query) 
   
    model_text = f"class {table_name}(models.Model):"
    for row in json:
        field_name = row['Field']
        field_type = row['Type']

        
        size_match = re.search(r'\((.*?)\)', field_type)
        size = size_match.group(1) if size_match else None

        if size and size.isdigit():
            size = f"max_length={size}"
        else:
            size = ""


        if 'int' in field_type and not 'tinyint' in field_type and not 'smallint' in field_type and not 'mediumint' in field_type and not 'bigint' in field_type:
            model_text += f"\n    {field_name} = models.IntegerField()"
        elif 'tinyint' in field_type:
            model_text += f"\n    {field_name} = models.BooleanField()"
        elif 'smallint' in field_type:
            model_text += f"\n    {field_name} = models.SmallIntegerField()"
        elif 'mediumint' in field_type:
            model_text += f"\n    {field_name} = models.IntegerField()"
        elif 'bigint' in field_type:
            model_text += f"\n    {field_name} = models.BigIntegerField()"
        elif 'varchar' in field_type or 'char' in field_type:
            model_text += f"\n    {field_name} = models.CharField({size})"
        elif 'text' in field_type or 'tinytext' in field_type or 'mediumtext' in field_type or 'longtext' in field_type:
            if 'tinytext' in field_type:
                model_text += f"\n    {field_name} = models.CharField(max_length=255)"
            else:
                model_text += f"\n    {field_name} = models.TextField()"
        elif 'date' in field_type:
            model_text += f"\n    {field_name} = models.DateField()"
        elif 'datetime' in field_type or 'timestamp' in field_type:
            model_text += f"\n    {field_name} = models.DateTimeField()"
        elif 'float' in field_type or 'double' in field_type:
            model_text += f"\n    {field_name} = models.FloatField()"
        elif 'decimal' in field_type:
            model_text += f"\n    {field_name} = models.DecimalField(max_digits=10, decimal_places=2)"
        elif 'bool' in field_type:
            model_text += f"\n    {field_name} = models.BooleanField()"
        elif 'enum' in field_type or 'set' in field_type:
            enum_values = re.findall(r"'\w+'", field_type)
            enum_values = [value.strip("'") for value in enum_values]
            choices = ", ".join([f"('{value}', '{value}')" for value in enum_values])
            model_text += f"\n    {field_name} = models.CharField(choices=[{choices}], max_length=255)"
        elif 'binary' in field_type or 'varbinary' in field_type or 'bit' in field_type or 'blob' in field_type or 'tinyblob' in field_type or 'mediumblob' in field_type or 'longblob' in field_type:
            model_text += f"\n    {field_name} = models.BinaryField()"
        elif 'json' in field_type:
            model_text += f"\n    {field_name} = models.JSONField()"
        elif 'geometry' in field_type:
            model_text += f"\n    {field_name} = models.GeometryField()"
        elif 'point' in field_type:     
            model_text += f"\n    {field_name} = models.PointField()"
        elif 'linestring' in field_type:
            model_text += f"\n    {field_name} = models.LineStringField()"
        elif 'polygon' in field_type:
            model_text += f"\n    {field_name} = models.PolygonField()"
        elif 'multipoint' in field_type:
            model_text += f"\n    {field_name} = models.MultiPointField()"
        elif 'multilinestring' in field_type:
            model_text += f"\n    {field_name} = models.MultiLineStringField()"
        elif 'multipolygon' in field_type:
            model_text += f"\n    {field_name} = models.MultiPolygonField()"
        elif 'uuid' in field_type:
            model_text += f"\n    {field_name} = models.UUIDField()"
        else:
            model_text += f"\n    {field_name} = models.CharField(max_length=255)"

    return HttpResponse(model_text, content_type='text/plain')

def get_head(request):
    head = """
    from django.shortcuts import redirect, get_object_or_404
    from django.http import JsonResponse
    from django.views.decorators.http import require_POST
    from .models import Connection
    import json\n\n
    """

    return head




def get_save(request): 
     
    table_name = request.POST.get("table_name")
    table_name_capitalized = table_name.capitalize()  
    query = f"describe {table_name}"           
    json = query_to_json(request,query) 

    view_text = get_head(request)
   
    view_text += f"def {table_name}_save(request):\n"

    view_text += "try:\n" 

    for row in json:       
        field_name = row['Field']   
        view_text += f"    {field_name} = request.POST.get('{field_name}')\n"

    view_text += "\n"
    view_text += f"    if id:\n"
    view_text += f"        obj_{table_name} =  get_object_or_404({table_name_capitalized},id=id)\n"
    view_text += f"    else:\n"
    view_text += f"        obj_{table_name} = {table_name_capitalized}()\n\n"

    for row in json:
        field_name = row['Field'] 
        view_text += f"    obj_{table_name}.{field_name} = {field_name}\n"  
        
    view_text += "\n"
    view_text += f"    obj_{table_name}.save()\n" 

    view_text += "\n"
    view_text += f"    return redirect('xxxxxxxx:xxxxxxxx')\n"

    view_text += "except Exception as e:\n"

    view_text += "    logging.error(f\"Error saving: {e}\")\n"
    view_text += "    return HttpResponseServerError(\"Error saving...\")\n"

    return view_text

def get_delete(request):
    table_name = request.POST.get("table_name")
    table_name_capitalized = table_name.capitalize()  
    query = f"describe {table_name}"           
    json = query_to_json(request,query) 

    view_text =  "@require_POST\n"
    view_text += f"def {table_name}_delete(request):\n"
    view_text += "try:\n"
    view_text += "    data = json.loads(request.body)\n"
    view_text += f"    {table_name}_id = data.get('id')\n"

    view_text += f"    obj_{table_name} = {table_name_capitalized}.objects.get(id={table_name}_id)\n"
    #view_text += f"    if obj_{table_name}:\n"
    view_text += f"    obj_{table_name}.status = 0\n"
    view_text += f"    obj_{table_name}.save()\n"
    view_text += "     return JsonResponse({'return': 'success'}, safe=False)\n"
    #view_text += "    else:\n"   
    view_text += "except Exception as e:\n"
    view_text += "     return JsonResponse({'error': str(e)}, status=400)"

    return view_text    

    
def get_view(request):
    view_text = get_save(request)
    view_text += "\n"
    view_text += get_delete(request)

    return HttpResponse(view_text, content_type='text/plain')