function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
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
        console.log(tableHtml); // Log the HTML to the console for debugging               
        document.getElementById('query-result').innerHTML = tableHtml;
    })
    .catch(error => {
        console.error('Error:', error);
    });
       
    }