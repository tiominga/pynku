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

    model_text = """
    from django.db import models
    from django.core.exceptions import ValidationError
    from django.contrib.auth.models import User
    from datetime import date

    """
   
    model_text += f"class {table_name}(models.Model):"
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
            model_text += f"\n    {field_name} = models.CharField(max_length=255)\n"

    model_text += "    date_created = models.DateField(auto_now_add=True)\n"

    model_text += """
    def clean(self):
       if self.xxxx =='':
          raise ValidationError('The xxx field cannot be empty.')

    """

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

    view_text += "    try:\n" 

    for row in json:       
        field_name = row['Field']   
        view_text += f"        {field_name} = request.POST.get('{field_name}')\n"

    view_text += "\n"
    view_text += f"        if id:\n"
    view_text += f"            obj_{table_name} =  get_object_or_404({table_name_capitalized},id=id)\n"
    view_text += f"        else:\n"
    view_text += f"            obj_{table_name} = {table_name_capitalized}()\n\n"

    for row in json:
        field_name = row['Field'] 
        view_text += f"        obj_{table_name}.{field_name} = {field_name}\n"  
        
    view_text += "\n"
    view_text += f"        obj_{table_name}.save()\n" 

    view_text += "\n"
    #view_text += f"    return redirect('xxxxxxxx:xxxxxxxx')\n"
    view_text += "        return JsonResponse({'return': 'success', 'message': 'Saved successfully.'})\n\n"

    view_text += "    except Exception as e:"

    view_text += """    
        logging.error(f"Error saving: {e}")
        return JsonResponse({'error': str(e)}, status=500)\n
    """

    #view_text += "    logging.error(f\"Error saving: {e}\")\n"
    #view_text += "    return HttpResponseServerError(\"Error saving...\")\n"

    return view_text

def get_delete(request):
    table_name = request.POST.get("table_name")
    table_name_capitalized = table_name.capitalize()  
    query = f"describe {table_name}"           
    json = query_to_json(request,query) 

    view_text =  "@require_POST\n"
    view_text += f"def {table_name}_delete(request):\n"
    view_text += "    try:\n"
    view_text += "        data = json.loads(request.body)\n"
    view_text += f"        {table_name}_id = data.get('id')\n"

    view_text += f"        obj_{table_name} = {table_name_capitalized}.objects.get(id={table_name}_id)\n"
    #view_text += f"    if obj_{table_name}:\n"
    view_text += f"        obj_{table_name}.status = 0\n"
    view_text += f"        obj_{table_name}.save()\n"
    view_text += "         return JsonResponse({'return': 'success', 'message': 'Deleted successfully.'}, safe=False)\n"
    #view_text += "    else:\n"   
    view_text += "    except Exception as e:\n"
    view_text += "         return JsonResponse({'error': str(e)}, status=400)"

    return view_text

def get_js_delete(request):
    table_name = request.POST.get("table_name")
    js_text = f"""
    function delete_{table_name}(){{
        if (confirm('Are you sure you want to delete this record?')) {{            
            let id = document.getElementById('id').value;
            fetch('/{table_name}/delete/', {{
                method: 'POST',
                headers: {{
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ id: id }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.return === 'success') {{
                    liveToast('bg-success', 'Deleted successfully.');
                    connection_list();
                }} else if (data.error) {{
                    liveToast('bg-danger', data.error);
                }} else {{
                    liveToast('bg-warning', 'Unexpected response.');
                }}
            }})
            .catch(error => {{
                liveToast('bg-danger', 'Network error: ' + error);
            }});
        }}
    }}
    """
    return js_text

def get_js_save(request):
    table_name = request.POST.get("table_name")
   
    js_text = """
    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    function save(){   
    """
    js_text += f"let formData = new FormData(document.getElementById('form_{table_name}'));\n"
    js_text += f"    fetch('/{table_name}/save/', "
    js_text += "{"

    js_text += """
    
     method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.return === 'success') {
            liveToast('bg-success', data.message || 'Saved successfully.');
            connection_list();
        } else if (data.error) {
            liveToast('bg-danger', data.error);
        } else {
            liveToast('bg-warning', 'Unexpected response.');
        }
    })
    .catch(error => {
        liveToast('bg-danger', 'Network error: ' + error);
    });
}
"""

    return js_text




def get_form(request):
    table_name = request.POST.get("table_name")
    columns = int(request.POST.get("columns", 1))  # Assume 1 coluna como padrão
    query = f"DESCRIBE {table_name}"
    json = query_to_json(request, query)
    
    # Adiciona o link para o Bootstrap no cabeçalho e CSS personalizado
    form_html = f"""
    <html>
    <head>
        <title>Formulário {table_name}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f2f2f2;
            }}
            .form-container {{
                background-color: #fff;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8 form-container">
                    <h2 class="text-center mb-4">Formulário {table_name}</h2>
                    <form id='form_{table_name}' method='POST' action='/{table_name}/save/'>
                        <div class='row'>
    """
    
    
    col_counter = 0

    for row in json:
        field_name = row['Field']
        field_type = row['Type']
        default_value = row.get('Default', '')

        if default_value in ['none', 'null', None, '']:
            default_value = ''

        size_match = re.search(r'\((.*?)\)', field_type)
        size = size_match.group(1) if size_match else None
        
        
        col_class = f"col-{12 // columns}"
        
        
        if 'id' in field_name.lower() or 'cod_id' in field_name.lower():
            form_html += f"        <input type='hidden' id='{field_name}' name='{field_name}' value='{default_value}'>\n"
            continue

        if col_counter == columns:
            form_html += "</div><div class='row'>"
            col_counter = 0

        form_html += f"    <div class='{col_class}'>\n"
        form_html += f"        <label for='{field_name}'>{field_name}</label>\n"
        
      
        if 'int' in field_type and not any(t in field_type for t in ['tinyint', 'smallint', 'mediumint', 'bigint']):
            form_html += f"        <input type='number' class='form-control' id='{field_name}' name='{field_name}' value='{default_value}'>\n"
        
        elif 'tinyint' in field_type:
            form_html += f"        <div class='form-check'>\n"
            form_html += f"            <input class='form-check-input' type='checkbox' id='{field_name}' name='{field_name}' {'checked' if default_value == '1' else ''}>\n"
            form_html += f"        </div>\n"
        
        elif 'varchar' in field_type or 'char' in field_type:
            form_html += f"        <input type='text' class='form-control' id='{field_name}' name='{field_name}' value='{default_value}'>\n"
        
        elif 'text' in field_type:
            form_html += f"        <textarea class='form-control' id='{field_name}' name='{field_name}'>{default_value}</textarea>\n"
        
        elif 'date' in field_type:
            form_html += f"        <input type='date' class='form-control' id='{field_name}' name='{field_name}' value='{default_value}'>\n"
        
        elif 'enum' in field_type:
            enum_values = re.findall(r"'\w+'", field_type)
            enum_values = [value.strip("'") for value in enum_values]
            form_html += f"        <select class='form-control' id='{field_name}' name='{field_name}'>\n"
            for value in enum_values:
                selected = "selected" if value == default_value else ""
                form_html += f"            <option value='{value}' {selected}>{value}</option>\n"
            form_html += f"        </select>\n"
        
        elif 'set' in field_type:
            enum_values = re.findall(r"'\w+'", field_type)
            enum_values = [value.strip("'") for value in enum_values]
            for value in enum_values:
                form_html += f"            <div class='form-check'>\n"
                form_html += f"                <input class='form-check-input' type='checkbox' name='{field_name}' value='{value}' id='{field_name}_{value}' {'checked' if value == default_value else ''}>\n"
                form_html += f"                <label class='form-check-label' for='{field_name}_{value}'>{value}</label>\n"
                form_html += f"            </div>\n"
        
        elif 'decimal' in field_type:
            form_html += f"        <input type='number' class='form-control' id='{field_name}' name='{field_name}' step='0.01' value='{default_value}' placeholder='R$ 0,00'>\n"
        
        else:
            form_html += f"        <input type='text' class='form-control' id='{field_name}' name='{field_name}' value='{default_value}'>\n"
        
        form_html += f"    </div>\n"
        col_counter += 1

    form_html += "</div>\n"
    form_html += f"<div class='row mt-3'>\n"
    form_html += f"    <div class='col-md-12 text-center'>\n"
    form_html += f"        <button type='submit' class='btn btn-primary'>Save</button>\n"
    form_html += f"    </div>\n"
    form_html += f"</div>\n"
    form_html += "</form>\n</div>\n</div>\n</div>\n</body>\n</html>"

    return HttpResponse(form_html, content_type='text/html')


############################################################################################    
def get_view(request):
    view_text = get_save(request)
    view_text += "\n"
    view_text += get_delete(request)
    


    return HttpResponse(view_text, content_type='text/plain')

def get_js_view(request):
    js_text = get_js_save(request)
    js_text += "\n"
    js_text += get_js_delete(request)
    
    return HttpResponse(js_text, content_type='text/plain')