function  liveToast(bg,message){


    $('#liveToast').removeClass('bg-primary bg-secondary bg-success bg-danger bg-warning bg-info bg-light bg-dark');
    $('#liveToast').addClass(bg);
    $('#toast-message').text(message);
 
 
    $('#liveToast').toast('show');
 
 
    var isSmallScreen = $(window).width() < 768; // Define 768 como limite para tela pequena
 
 
    if (isSmallScreen){
     let t = $('#bt_salvar').offset().top-30;
     $('#liveToast').offset({ top: t });
    }
 
 }

 function editor_model(){
    var selected_table = document.querySelector('input[name="rb_table"]:checked');
    console.log(selected_table.value);
    url = '/editor/get_model';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({ 'table_name': selected_table.value })
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('query-result').innerText = text;
    })
    .catch(error => console.error('Erro:', error));
}

function editor_view(){
    var selected_table = document.querySelector('input[name="rb_table"]:checked');
    console.log(selected_table.value);
    url = '/editor/get_view';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({ 'table_name': selected_table.value })
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('query-result').innerText = text;
    })
    .catch(error => console.error('Erro:', error));
}

function editor_js_view(){
    var selected_table = document.querySelector('input[name="rb_table"]:checked');
    console.log(selected_table.value);
    url = '/editor/get_js_view';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: new URLSearchParams({ 'table_name': selected_table.value })
    })
    .then(response => response.text())
    .then(text => {
        document.getElementById('query-result').innerText = text;
    })
    .catch(error => console.error('Erro:', error));
}

function editor_form(){
    var selected_table = document.querySelector('input[name="rb_table"]:checked');
      
    var numColumns = prompt("How much columns?", "1");
   
    if (!numColumns || isNaN(numColumns) || numColumns <= 0) {
        numColumns = 1;
    }
  
    var url = '/editor/get_form';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()  
        },
        body: new URLSearchParams({
            'table_name': selected_table.value,
            'columns': numColumns
        })
    })
    .then(response => response.text())
    .then(text => {        
        document.getElementById('query-result').textContent = text;
    })
    .catch(error => console.error('Erro:', error));
}



   
