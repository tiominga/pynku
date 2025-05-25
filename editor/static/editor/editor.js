function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function history_click(sql) {

    exec_sql(sql);
    editor.setValue(sql);

}    

function sql_string_works(sql) {

    sql = sql.trim();
    sql = sql.replace(/\s+/g, ' '); // Remove extra spaces 
    sql = sql.substring(0, 50); // Limit to 1000 characters 
    return sql;

}    

function add_history(sql) {
  
 sql_view = sql_string_works(sql);   
 const ul = document.getElementById("sql-history");
 const li = document.createElement("li");
 li.textContent = sql_view;
 li.dataset.sql = sql;
 li.addEventListener("click", () => history_click(sql));
 li.className = "sql-history-item";
 li.title = sql;
 ul.insertBefore(li,ul.firstChild);   

}

function exec_sql(sql){
    
    if (!sql || sql.length == 0) {
        sql = editor.getValue();
    }      
    
    fetch('/editor/get_table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({ 'query': sql })
    })
    .then(response => response.json())  
    .then(data => {        
        const tableHtml = data.html;         
        document.getElementById('query-result').innerHTML = tableHtml;

        let editor_text = editor.getValue();
        if (editor_text.length == 0) {
           editor.setValue(sql); 
        }

        add_history(sql);
    })
    .catch(error => {
        console.error('Error:', error);
    });
       
    }

    function run(e){
        alert('1');
        if (e.key === "F9"){

            alert('oi');

        }


    }