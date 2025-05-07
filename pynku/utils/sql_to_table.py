from django.db import connections
from django.utils.html import escape
from django.urls import reverse
from connection.models import Connection
from pynku.utils.db_connection import get_connection

class SqlToTable:
    def __init__(self):
        self.query = None
        self.params = None
        self.edit_rout = None
        self.delete_rout = None

    def set_query(self, query):
        self.query = query

    def set_params(self, params):
        self.params = params

    def set_edit_rout(self, edit_rout):
        self.edit_rout = edit_rout

    def set_delete_rout(self, delete_rout):
        self.delete_rout = delete_rout

    def execute_query(self, request):
        cursor = get_connection(request)
        try:
            cursor.execute(self.query, self.params or [])
        except Exception as e:
            return str(e) 

        try:
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return result, columns
        except:
            return "Success..."

    def get_buttons(self, id_value):
       
        return ""

    def query_to_html(self, request):
        resultado = self.execute_query(request)

        if isinstance(resultado, str):
            # Verifica se a mensagem parece ser um erro (pode ajustar essa lógica se quiser)
            if "error" in resultado.lower() or "syntax" in resultado.lower():
                return f"<div class='alert alert-danger'>{escape(resultado)}</div>"
            else:
                return f"<div style='background-color: #007bff; color: white; padding: 10px; border-radius: 5px;'>{escape(resultado)}</div>"

        result, columns = resultado

        # Renderiza a tabela normalmente
        table_html = '<table class="table table-bordered table-striped">'
        table_html += '<thead><tr>'
        for column in columns:
            table_html += f'<th>{escape(column)}</th>'
        table_html += '</tr></thead><tbody>'

        for row in result:
            table_html += '<tr>'
            for column in row:
                table_html += f'<td>{escape(str(column))}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'

        return table_html

