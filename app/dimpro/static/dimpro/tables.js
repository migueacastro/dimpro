let dataTable;
let dataTableIsInitialized=false;
function ShowDataTable (dataTableModel) {
    const initDataTable=async()=>{
        if(dataTableIsInitialized){
            dataTable.destroy();
        }
        await dataTableModel();
        dataTable = $('#datatable-orders').DataTable({
            "retrieve": true,
            "language": {
                "sProcessing":    "Procesando...",
                "sLengthMenu":    "Mostrar _MENU_ registros",
                "sZeroRecords":   "No se encontraron resultados",
                "sEmptyTable":    "Ningún dato disponible",
                "sInfo":          "",
                "sInfoEmpty":     "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered":  "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix":   "",
                "sSearch":        "Buscar:",
                "sUrl":           "",
                "sInfoThousands":  ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst":    "Primero",
                    "sLast":    "Último",
                    "sNext":    "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            }
        });
    
        dataTableIsInitialized = true;
    };

    window.addEventListener('load',async()=>{
        await initDataTable();
    });
}

function editDataTable (dataTableModel) {
    const initDataTable=async()=>{
        if(dataTableIsInitialized){
            dataTable.destroy();
        }
        await dataTableModel();
        dataTable = $('#datatable-orders').DataTable({
            "paging": false,
            "retrieve": true,
            "searching": false,
            "language": {
                "sProcessing":    "Procesando...",
                "sLengthMenu":    "Mostrar _MENU_ registros",
                "sZeroRecords":   "No se encontraron resultados",
                "sEmptyTable":    "Ningún dato disponible en esta tabla",
                "sInfo":          "",
                "sInfoEmpty":     "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered":  "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix":   "",
                "sSearch":        "Buscar:",
                "sUrl":           "",
                "sInfoThousands":  ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst":    "Primero",
                    "sLast":    "Último",
                    "sNext":    "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            }
        });
    
        dataTableIsInitialized = true;
    };

    window.addEventListener('load',async()=>{
        await initDataTable();
    });
}


const listOrders=async()=>{
    try {
        let response;
        let url = window.location.href;
        let parts = url.split('/');
        let lastNumber = parts[parts.length - 2];
        let isUser = document.body.dataset.isUser === 'true';
        if (!isNaN(lastNumber) && lastNumber != "") {
            response=await fetch(`/app/list_orders/user/${lastNumber}/`);
        }
        else {
            response=await fetch('/app/list_orders/');
        }
        
        const data= await response.json();

        let content=``;
        data.orders.forEach((order, index)=>{
            if ((!isNaN(lastNumber) && lastNumber != "") || order.products > 0) {
                if (isUser) {
                    content+=`
                <tr class="clickable-row" data-href="/app/client/order/view/${order.id}">
                    <td>${order.id}</td>`;
                }
                else {
                    content+=`
                <tr class="clickable-row" data-href="/app/staff/view/order/${order.id}">
                    <td>${order.id}</td>`; }
                if (isNaN(lastNumber)) {
                    content += `<td>${order.user_email}</td>`;
                }
                content+=`
                    <td>${order.client_name}</td>
                    <td>${order.products}</td>
                    `;
                if (order.status == 'Pendiente') {
                    content += `<td><p class="m-2 p-2 red-bg rounded text-center second-text grow mx-auto">Pendiente</p></td>`;
                }
                else {
                    content += `<td><p class="m-2 p-2 rounded text-center second-text grow mx-auto" style="background-color: var(--main-bg-color) !important;">Preparado</p></td>`;
                }

                content += `
                    <td>${order.date}</td>
                </tr>
                `;
            }
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        console.log(ex);
    }
};


const listOrdersAll=async()=>{
    try {
        let response;
        response=await fetch('/app/list_orders/all/');

        
        const data= await response.json();

        let content=``;
        data.orders.forEach((order, index)=>{
            if (order.products > 0) {
                content+=`
                <tr class="clickable-row" data-href="/app/staff/view/order/${order.id}">
                    <td>${order.id}</td>
                    <td>${order.user_email}</td>
                    <td>${order.client_name}</td>
                    <td>${order.products}</td>
                `;
                if (order.status == 'Pendiente') {
                    content += `<td><p class="m-2 p-2 red-bg rounded text-center second-text grow mx-auto">Pendiente</p></td>`;
                }
                else {
                    content += `<td><p class="m-2 p-2 rounded text-center second-text grow mx-auto" style="background-color: var(--main-bg-color) !important;">Preparado</p></td>`;
                }

                content += `
                    <td>${order.date}</td>
                </tr>
                `;
            }
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};

const listSellers=async()=>{
    try {
        const response=await fetch('/app/list_sellers/');
        const data= await response.json();

        let content=``;
        data.sellers.forEach((user, index)=>{
            content+=`
                <tr class="clickable-row" data-href="/app/staff/view/seller/${user.id}">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.orders}</td>
                    <td>${user.phonenumber}</td>     
            `;
            let isOperator = document.body.dataset.isOperator === 'True';
            if (isOperator) {
                content += `
                    <td><a class="primary-text" href="/app/staff/delete/${user.id}">
                    <i class="fa-solid fa-trash-can"></i>
                    </a></td>`;
            }
            content+=`</tr>`;
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};

const listEmployees=async()=>{
    try {
        const response=await fetch('/app/list_employees/');
        const data= await response.json();

        let content=``;
        data.employees.forEach((user, index)=>{
            content+=`
                <tr class="clickable-row" data-href="/app/staff/view/seller/${user.id}">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.phonenumber}</td>
                    <td><a class="primary-text" href="/app/staff/delete/${user.id}">
                    <i class="fa-solid fa-trash-can"></i>
                    </a></td>
                </tr>
            `;
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};

$(document).ready(function($) {
    $(document).on('click', '.clickable-row', function() {
        window.location.replace($(this).data("href"));
    });
});

const listOrderProducts=async()=>{
    try {
        let response;
        
        let url = window.location.href;
        let parts = url.split('/');
        let lastNumber = parts[parts.length - 1];
        if (lastNumber === "") {
            lastNumber = parts[parts.length - 2];
        }
        response=await fetch(`/app/list_products_order/order/${lastNumber}/`);
        const data= await response.json();

        let content=``;
        data.products.forEach((product, index)=>{
            content+=`
            <tr id="${index}">
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.reference}</td>
                <td>${product.quantity}</td>
                <td>${product.price}$</td>
                <td>${product.cost}$</td>
            </tr>
            `;
            
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};

var product_data;

const listOrderProductsEdit=async()=>{
    try {
        let response;
        document.getElementById('total').innerText = document.getElementById('total-tosubmit').value + '$';
        let product_search = await fetch("/app/list_products/");
        let url = window.location.href;
        let parts = url.split('/');
        let lastNumber = parts[parts.length - 2];
        response=await fetch(`/app/list_products_order/order/${lastNumber}/`);
        product_data = await product_search.json();
        const data= await response.json();

        let content=``;
        data.products.forEach((product, index)=>{
            let id;
            let reference;
            let availability;
            let item_name;
            product_data.products.forEach((item) => {
                if (item.id == product.id){
                    id = item.id;
                    item_name = item.item;
                    reference = item.reference;
                    availability = item['available-quantity'];
                }
            });
            
            if ((id == null)) {
                id = "Indefinido";
                reference = "Sin referencia";
            }


            content+=`
            <tr id="${index}">
                <td id="id-${index}">${id}</td>
                <td>
                    <input id="item-${index}" required class="form-control" 
                    onchange="setInputValue('item-${index}', product_data); changeValues('id-${index}', 'reference-${index}', 'aq-${index}', 'item-q-${index}', 'item-${index}', 'price-${index}', 'cost-${index}'); verify();"
                    type="text" list="product-selection" value="${product.name}"</input></td>
                <td id="reference-${index}">${reference}</td>
                <td><input id="item-q-${index}" required  type="number" class="form-control" min="1" max="${product['available-quantity']}" value="${product.quantity}" onfocus="changeNumbers('item-q-${index}', 'item-q-${index}', 'price-${index}', 'cost-${index}')"></input></td>
                <td id="aq-${index}">${product['available-quantity']}</td>
                <td id="price-${index}">${product.price}$</td>
                <td id="cost-${index}">${(parseDollar(product.price*product.quantity))}$</td>
                <td><i class="fa-solid fa-xmark grow" onclick="deleteRow(${index});"></i></td>
            </tr>
            `;
           
            
            
            
            
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        console.log(ex);
    }
    updateTotal();
};
var product_data;
var inputId;
var lastSelectedItem;
function setInputValue(input, product_data) {
    inputId = input;
    var input = document.getElementById(inputId);
    id = input.id.charAt(input.id.length - 1);
    
    var valor = input.value;
    var datalist = document.getElementById('product-selection');

    var rows = document.getElementById('datatable-orders').rows;

    var itemCounts = {};
    console.log(rows.length);
    for (var i = 0; i < rows.length -1; i++) {

        var row = document.getElementById(i);
        if (row) {
            if (row.style.display === 'none') {
                continue;
            }
    
            var item = document.getElementById('item-' + i).value;
    
            itemCounts[item] = (itemCounts[item] || 0) + 1;
    
            if (valor === item && itemCounts[item] > 1) {
                console.log('El producto ya existe en la tabla');
                input.value = '';
                input.placeholder = 'El producto ya existe';
                document.getElementById('price-'+id).innerText = '';
                document.getElementById('cost-'+id).innerText = '';
                return;  // Termina la ejecución de la función aquí
            }
            if (item !== null && item !== '' && i == inputId.charAt(inputId.length -1)) {
                duplicateRow(i);
            }    
        }
        

    }
    var selectedItem = input.value;
    lastSelectedItem = selectedItem;
}

var lastSelectedItem = null;

function verify() {
    var input = document.getElementById(inputId);
    var valor = input.value;
    var datalist = document.getElementById('product-selection');
    var options = datalist.options;
    var exists = false;

    for (var i = 0; i < options.length; i++) {
        if (valor == options[i].value) {
            exists = true;
            break;
        }
    }

    if (!exists && valor !== '') {
        input.value = '';
        input.placeholder = '';
    } else {
        lastSelectedItem = valor;
    }
}





async function changeValues (id, reference, aq, q, name, price, cost) {
    let value = document.getElementById(name).value;
    let v1 = "";
    let v2 = "";
    let v3 = "";
    let v4 = "";
    let v5 = "";
    let response = await fetch("/app/list_products/");
    let product_search = await response.json();
    product_search.products.forEach((product) => {
        if (product.item == value){
            v1 = product.id;
            v2 = product.reference;
            v3 = product['available_quantity'];
            v4 = 1;
            v5 = product.price;
        }
        
    });
    document.getElementById(id).innerText = v1;
    document.getElementById(reference).innerText = v2;
    document.getElementById(aq).innerText = v3;
    document.getElementById(q).value = v4;
    document.getElementById(q).max = v3;
    if (v5 === "") {
        document.getElementById(price).innerText = '';
        document.getElementById(cost).innerText = '';
    }
    else {
        document.getElementById(price).innerText = parseDollar(v5) + '$';
        document.getElementById(cost).innerText = parseDollar(v5) + '$';
    }
    updateTotal();
}

async function changeNumbers (id, q, price, cost) {
    
    

    input = document.getElementById(id);
    input.addEventListener('change', function() {
        let v4 = document.getElementById(q).value;
        let v5 = document.getElementById(price).innerText; 
        let v6 = (parseDollar(v5) * parseDollar(v4));
        if (isNaN(v6)) {
            document.getElementById(cost).innerText = '';
        }
        else {
            document.getElementById(cost).innerText = parseDollar(v6)+'$';
        }
        
        updateTotal();
    }) 
}

function parseDollar(n) {
    return (parseFloat(n.toString().replace(/\$/,'')).toFixed(2));
}

function updateTotal(n) {
    let table = document.getElementById('tableBody_orders');
    let total = 0;
        for (let i =  0; i < table.rows.length; i++) {
            if (document.getElementById(i).style.display === 'none') {
                if (document.getElementById('cost-d-'+i)) {
                    numbertosum = -(parseFloat(parseDollar(document.getElementById('cost-d-'+i).innerText)));
                }
                continue;
            }
            else {
                numbertosum = parseFloat(parseDollar(document.getElementById('cost-'+i).innerText));
            }
            
            if (isNaN(numbertosum)) {
                continue;
            }
            total = parseFloat(total) + numbertosum;
        };
    document.getElementById('total-tosubmit').value = parseDollar(total);
    document.getElementById('total').innerText = parseDollar(total)+'$';
}
function addRow() {

    let index = document.getElementById('tableBody_orders').rows.length;
    
    var element = document.querySelector('.dataTables_empty');
    if (element) {
        var parentElement = element.parentElement;
            if (parentElement) {
                parentElement.style.display = 'none';
            }
    }
    
    
    let table = document.getElementById('tableBody_orders');

    let row = document.createElement('tr');
    row.id = index;

    let cell1 = document.createElement('td');
    cell1.id = `id-${index}`;
    let cell2 = document.createElement('td');
    let cell3 = document.createElement('td');
    cell3.id = `reference-${index}`;
    let cell4 = document.createElement('td');
    let cell5 = document.createElement('td');
    cell5.id = `aq-${index}`;
    let input1 = document.createElement('input');
    let cell6 = document.createElement('td');
    cell6.id = `price-${index}`;
    let cell7 = document.createElement('td');
    cell7.id = `cost-${index}`;
    let cell8 = document.createElement('td');
    input1.id = 'item-' + index;
    input1.required = true;
    input1.className = 'form-control';
    input1.type = 'text';
    input1.setAttribute('list', 'product-selection');
    input1.value = '';
    input1.onchange = function() {
        setInputValue('item-' + index, product_data);
        changeValues('id-' + index, 'reference-' + index, 'aq-' + index, 'item-q-' + index, 'item-' + index, 'price-' + index, 'cost-' + index);
        verify(index);  // Pasar 'index' como parámetro
    };
    

    let input2 = document.createElement('input');
    input2.id = 'item-q-' + index;
    input2.required = true;
    input2.type = 'number';
    input2.className = 'form-control';
    input2.min = '1';
    input2.value = '';
    input2.onchange = function () {
        changeNumbers('item-q-' + index, 'item-q-' + index, 'price-' + index, 'cost-' + index);
    }
    let icon = document.createElement('i');
    icon.className = 'fa-solid fa-xmark';
    icon.onclick = function() {
        deleteRow(index);
    };
    
    cell2.appendChild(input1);
    cell4.appendChild(input2);
    cell8.appendChild(icon);

    row.appendChild(cell1);
    row.appendChild(cell2);
    row.appendChild(cell3);
    row.appendChild(cell4);
    row.appendChild(cell5);
    row.appendChild(cell6);
    row.appendChild(cell7);
    row.appendChild(cell8);
    table.appendChild(row);
    
}


function duplicateRow(id) {
    let table = document.getElementById('tableBody_orders');
    let index = table.rows.length;
    let originalRow = document.getElementById(id);

    // Clona la fila original
    let clonedRow = originalRow.cloneNode(true);

    clonedRow.id = index;

    clonedRow.querySelector('#id-' + id).id = 'id-' + index;
    clonedRow.querySelector('#item-' + id).id = 'item-' + index;
    clonedRow.querySelector('#item-' + index).onchange = function() {
        setInputValue('item-' + id, product_data);
        changeValues('id-' + index, 'reference-' + index, 'aq-' + index, 'item-q-' + index, 'item-' + index, 'price-' + index, 'cost-' + index);
        verify();
    };
    clonedRow.querySelector('#reference-' + id).id = 'reference-' + index;

    clonedRow.querySelector('#item-q-' + id).id = 'item-q-' + index;
    clonedRow.querySelector('#price-' + id).id = 'price-' + index;
    clonedRow.querySelector('#cost-' + id).id = 'cost-' + index;
    clonedRow.querySelector('#aq-' + id).id = 'aq-' + index;
    input2 = clonedRow.querySelector('#item-' + index);
    input2.removeAttribute('required');
    input = clonedRow.querySelector('#item-q-' + index);
    input.setAttribute('min', '0');
    input.setAttribute('max', '0')
    input.setAttribute('value', '0');
    input.removeAttribute('required');
    clonedRow.style.display = 'none'; 
    originalRow.parentNode.appendChild(clonedRow);
    updateTotal();
}

function deleteRow(id) {
    let table = document.getElementById('tableBody_orders');
    let index = table.rows.length;

    let originalRow = document.getElementById(id);
    originalRow.querySelector('#item-' + originalRow.id).removeAttribute('required');
    document.getElementById('item-q-' + originalRow.id).setAttribute('min', '0');
    document.getElementById('item-q-' + originalRow.id).setAttribute('value', '0');
    document.getElementById('item-q-' + originalRow.id).removeAttribute('required');
    document.getElementById('cost-' + originalRow.id).setAttribute('id', 'cost-d-'+ originalRow.id);
    originalRow.style.display = 'none';
    updateTotal();
}

function postData() {
    let table = document.getElementById('tableBody_orders');
    let data = [];

    
    let url = window.location.href;
    let parts = url.split('/');
    let lastNumber = parts[parts.length - 2];

    for (let i =  0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let rowIndex = row.id;

        let item = document.getElementById('item-' + rowIndex);

        if (item) {
            item = item.value;
        }
        else {
            continue;
        }

        let reference = document.getElementById('reference-' + rowIndex).value;

        let cost;
        let quantity;
        if (row.style.display == 'none') {
            quantity = 0;
            cost = 0;
        }
        else {
            quantity = document.getElementById('item-q-'+ rowIndex).value;
            cost = parseDollar(document.getElementById('cost-' + rowIndex).innerText);
        }
        
        

        let exists = data.some(function(el) {
            return el.item === item;
        })
        
        if (!exists || quantity > 0) {
            data.push({
                item: item,
                reference: reference,
                cost: cost,
                quantity: quantity
            });
        }
        
    }
    let isUser = document.body.dataset.isUser === 'true';
    if (isUser) {
        fetch(`/app/client/order/edit/${lastNumber}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf').innerText
            },
    
            body: JSON.stringify(data),
        })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(data => {
            console.log(('Success:'), data);
        })
        .catch((error) => {
            console.log('Error:', error);
        });
    }
    else {
        fetch(`/app/staff/view/order/edit/${lastNumber}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf').innerText
            },
    
            body: JSON.stringify(data),
        })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .then(data => {
            console.log(('Success:'), data);
        })
        .catch((error) => {
            console.log('Error:', error);
        });
    }
    
    
}

