var arr_connections = null;

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function connection_save(){


    if ( document.getElementById('project_add_combo').style.display == 'block'){

        let select = document.getElementById('select_name');
        let selectedText = select.options[select.selectedIndex].text;
        document.getElementById('name').value = selectedText;
        
    }

    f_orm = document.getElementById('form_connection');
    f_orm.submit();

}

function connection_connect(){

    connection_save();

}

function connection_delete(){

    if (confirm("Are you sure you want to delete this connection?")) {
        var url = '/connection/delete/';
        let id = document.getElementById('select_name').value;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
               
        },
        body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.return) {
                alert("Connection deleted successfully.");
                connection_list();
            } else {
                alert("Error deleting connection.");
            }
        });
    }
}   


function connection_select(){

    document.getElementById('project_add').style.display = 'none';
    document.getElementById('project_add_combo').style.display = 'block';
    document.getElementById('bt_connect').innerText = 'Connect..';

}    

function connection_new(){

    f_orm = document.getElementById('form_connection');    
    f_orm.reset();
    document.getElementById('project_add').style.display = 'block';
    document.getElementById('project_add_combo').style.display = 'none';

    document.getElementById('bt_connect').innerText = 'Save and Connect..';

}


function connection_change(id){
    
    let data = arr_connections.find(p => p.id == id);
    if (data) {        
        document.getElementById('name').value = data.name;
        document.getElementById('host').value = data.host;  
        document.getElementById('port').value = data.port;
        document.getElementById('user').value = data.user;  
        document.getElementById('password').value = data.password;
        document.getElementById('database').value = data.database;
        document.getElementById('id').value = data.id;

    }

}

function connection_list(){

    var url = '/connection/list/';
    fetch(url)
        .then(response => response.json())
        .then(data=> {

          arr_connections = data;  
          var options = "";
          var cont = 0;

          data.forEach(item => {
            
            let projet_name = item.name;
            let projet_id = item.id;

            options += "<option value=" + projet_id + ">" + projet_name + "</option>";

            if (cont == 0){
                connection_change(projet_id);
            }

            cont++;

          });

         document.getElementById('select_name').innerHTML = options;

        });    
    
}


 