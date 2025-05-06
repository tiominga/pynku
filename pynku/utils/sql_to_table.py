from django.db import connections
from django.utils.html import escape
from django.urls import reverse

class SqlToTable:
    def __init__(self):
        self.query = None
        self.params = None
        self.edit_rout = None  # Ex: 'form' (name da URL)
        self.delete_rout = None  # Ex: 'delete_viagem'

    def set_query(self, query):
        self.query = query

    def set_params(self, params):
        self.params = params

    def set_edit_rout(self, edit_rout):
        self.edit_rout = edit_rout

    def set_delete_rout(self, delete_rout):
        self.delete_rout = delete_rout

    def execute_query(self):
        with connections['default'].cursor() as cursor:
            cursor.execute(self.query, self.params)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        return result, columns

    def get_buttons(self, id_value):
        buttons = ""

        if self.edit_rout is not None:
            edit_url = reverse(self.edit_rout, kwargs={'id': id_value})
            buttons += f'<a href="{edit_url}" class="btn btn-primary btn-sm mr-2" style="padding: 0.2rem 0.4rem;">Alterar</a>'

        if self.delete_rout is not None:
            delete_url = reverse(self.delete_rout, kwargs={'id': id_value})
            buttons += f'<a href="{delete_url}" class="btn btn-danger btn-sm" style="padding: 0.2rem 0.4rem;">Excluir</a>'

        return buttons

    def query_to_html(self):
        result, columns = self.execute_query()

        # Índice da coluna "id"
        try:
            id_index = columns.index("id")
        except ValueError:
            raise Exception("A consulta SQL deve retornar uma coluna chamada 'id'.")

        # Criando a tabela HTML com Bootstrap
        table_html = '<table class="table table-bordered table-striped">'

        # Cabeçalhos
        table_html += '<thead><tr>'
        for column in columns:
            table_html += f'<th>{escape(column)}</th>'
        table_html += '<th>Ações</th></tr></thead>'

        # Corpo da tabela
        table_html += '<tbody>'
        for row in result:
            table_html += '<tr>'
            for column in row:
                table_html += f'<td>{escape(str(column))}</td>'

            row_id = row[id_index]
            buttons = self.get_buttons(row_id)
            table_html += f'<td>{buttons}</td></tr>'
        table_html += '</tbody></table>'

        return table_html
