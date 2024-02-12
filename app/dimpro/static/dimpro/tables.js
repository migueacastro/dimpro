let dataTable;
let dataTableIsInitialized=false;
let hasId=false;
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
        if (hasId) {
            let url = window.location.href;
            let parts = url.split('/');
            let lastNumber = parts[parts.length - 1];
            response=await fetch(`/app/list_orders/user/${lastNumber}`);
        }
        else {
            response=await fetch('/app/list_orders/');
        }
        
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
                    <td><p class="red-bg rounded text-center second-text grow mx-auto">${order.status}</p></td>
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
        response=await fetch(`/app/list_products_order/order/${lastNumber}`);
        const data= await response.json();

        let content=``;
        data.products.forEach((product, index)=>{
            content+=`
            <tr id="${index}">
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.reference}</td>
                <td>${product.quantity}</td>
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
        let product_search = await fetch("/app/list_products/");
        let url = window.location.href;
        let parts = url.split('/');
        let lastNumber = parts[parts.length - 1];
        response=await fetch(`/app/list_products_order/order/${lastNumber}`);
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
                    onchange="setInputValue('item-${index}', product_data); duplicateRow(${index}); changeValues('id-${index}', 'reference-${index}', 'aq-${index}', 'item-q-${index}', 'item-${index}'); verify();"
                    type="text" list="product-selection" value="${product.name}"</input></td>
                <td id="reference-${index}">${reference}</td>
                <td><input id="item-q-${index}" required  type="number" class="form-control" min="1" max="${product['available-quantity']}" value="${product.quantity}"></input></td>
                <td id="aq-${index}">${product['available-quantity']}</td>
                <td><i class="fa-solid fa-xmark grow" onclick="deleteRow(${index});"></i></td>
            </tr>
            `;
           
            
            
            
            
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};
var product_data;
var inputId;
var lastSelectedItem;
function setInputValue(input, product_data) {
    inputId = input;
    var input = document.getElementById(inputId);
    var valor = input.value;
    var datalist = document.getElementById('product-selection');

    var rows = document.getElementById('datatable-orders').rows;

    var itemCounts = {};
    console.log(rows.length);
    for (var i = 0; i < rows.length -1; i++) {

        var item = document.getElementById('item-' + i).value;

        itemCounts[item] = (itemCounts[item] || 0) + 1;

        if (valor === item && itemCounts[item] > 1) {
            console.log('El producto ya existe en la tabla');
            input.value = '';
            input.placeholder = 'El producto ya existe';
            return;  // Termina la ejecución de la función aquí
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





async function changeValues (id, reference, aq, q, name) {
    let value = document.getElementById(name).value;
    let v1 = "";
    let v2 = "";
    let v3 = "";
    let v4 = "";
    let response = await fetch("/app/list_products/");
    let product_search = await response.json();
    product_search.products.forEach((product) => {
        if (product.item == value){
            v1 = product.id;
            v2 = product.reference;
            v3 = product['available_quantity'];
            v4 = 1;
        }
        
    });
    document.getElementById(id).innerText = v1;
    document.getElementById(reference).innerText = v2;
    document.getElementById(aq).innerText = v3;
    document.getElementById(q).value = v4;
    document.getElementById(q).max = v3;
}

function addRow() {
    let index = document.getElementById('tableBody_orders').rows.length;
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
    input1.id = 'item-' + index;
    input1.required = true;
    input1.className = 'form-control';
    input1.type = 'text';
    input1.setAttribute('list', 'product-selection');
    input1.value = '';
    input1.onchange = function() {
        setInputValue('item-' + index, product_data);
        duplicateRow(index);  // Pasar 'index' como parámetro
        changeValues('id-' + index, 'reference-' + index, 'aq-' + index, 'item-q-' + index, 'item-' + index);
        verify(index);  // Pasar 'index' como parámetro
    };
    

    let input2 = document.createElement('input');
    input2.id = 'item-q-' + index;
    input2.required = true;
    input2.type = 'number';
    input2.className = 'form-control';
    input2.min = '1';
    input2.value = '';

    let icon = document.createElement('i');
    icon.className = 'fa-solid fa-xmark';
    icon.onclick = function() {
        deleteRow(index);
    };

    cell2.appendChild(input1);
    cell4.appendChild(input2);
    cell6.appendChild(icon);

    row.appendChild(cell1);
    row.appendChild(cell2);
    row.appendChild(cell3);
    row.appendChild(cell4);
    row.appendChild(cell5);
    row.appendChild(cell6);
    table.appendChild(row);
}


function duplicateRow(id) {
    let table = document.getElementById('tableBody_orders');
    let index = table.rows.length;
    let originalRow = document.getElementById(id);

    // Clona la fila original
    let clonedRow = originalRow.cloneNode(true);

    clonedRow.id = index;

    clonedRow.querySelector('#item-' + id).id = 'item-' + index;
    

    clonedRow.querySelector('#reference-' + id).id = 'reference-' + index;

    clonedRow.querySelector('#item-q-' + id).id = 'item-q-' + index;

    clonedRow.querySelector('#aq-' + id).id = 'aq-' + index;

    input = clonedRow.querySelector('#item-q-' + index);
    input.min = '0';
    input.max = '0';
    input.setAttribute('value', '0');
    
    clonedRow.style.display = 'none'; // Aquí está la corrección
    originalRow.parentNode.appendChild(clonedRow);

}

function deleteRow(id) {
    let table = document.getElementById('tableBody_orders');
    let index = table.rows.length;

    let originalRow = document.getElementById(id);

    // Clona la fila original
    let clonedRow = originalRow.cloneNode(true);

    clonedRow.id = index + 1;

    clonedRow.querySelector('#item-' + id).id = 'item-' + index;

    clonedRow.querySelector('#reference-' + id).id = 'reference-' + index;

    clonedRow.querySelector('#item-q-' + id).id = 'item-q-' + index;

    clonedRow.querySelector('#aq-' + id).id = 'aq-' + index;

    clonedRow.style.display = 'none';

    originalRow.parentNode.appendChild(clonedRow);
    document.getElementById('item-q-' + index).setAttribute('value', '0');
    originalRow.parentNode.removeChild(originalRow);
}