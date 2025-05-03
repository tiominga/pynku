from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Connection
import json

# Create your views here.


@require_POST
def connection_delete(request):
    try:
        data = json.loads(request.body)
        connection_id = data.get('id')

        obj_connection = Connection.objects.get(id=connection_id)
        if obj_connection:
            obj_connection.status = 0
            obj_connection.save()
            return JsonResponse({'return': 'success'}, safe=False)
        else:
            return JsonResponse({'return': 'error'}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)    



def connection_list(request):
    connections = Connection.objects.filter(status=1)
    data = [
        {
            'id': item.id,
            'name': item.name,
            'host': item.host,
            'port': item.port,
            'user': item.user,
            'password': item.password,
            'database': item.database,
        }
        for item in connections
    ]
    return JsonResponse(data, safe=False)


def connection_save(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        id = request.POST.get('id')

        if id:
            obj_connection = Connection.objects.get(id=id)
        else:
            obj_connection = Connection()    
           
        obj_connection.name = name
        obj_connection.host = host
        obj_connection.port = port
        obj_connection.user = user
        obj_connection.password = password
        obj_connection.database = database
        

        obj_connection.save() 

        request.session['id_connection'] = obj_connection.id   
         

    return redirect('editor:editor')
