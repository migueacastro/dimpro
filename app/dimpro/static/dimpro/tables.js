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
                    onchange="setInputValue('item-${index}', product_data); changeValues('id-${index}', 'reference-${index}', 'aq-${index}', 'item-q-${index}', 'item-${index}'); verify();"
                    type="text" list="product-selection" value="${product.name}"</input></td>
                <td id="reference-${index}">${reference}</td>
                <td><input id="item-q-${index}" required  type="number" class="form-control" min="1" max="${product['available-quantity']}" value="${product.quantity}"></input></td>
                <td id="aq-${index}">${product['available-quantity']}</td>
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
    
    var datalist = document.getElementById('product-selection');

    var selectedItem = input.value;
    lastSelectedItem = selectedItem;

    var newOptions = product_data.products.filter(item => item.item !== selectedItem);

    while (datalist.firstChild) {
        datalist.removeChild(datalist.firstChild);
    }
    
    newOptions.forEach((item) => {
        var option = document.createElement('option');
        option.value = item.item;
        datalist.appendChild(option);
    });

    input.value = selectedItem;
}

function verify() {
    var input = document.getElementById(inputId);
    
    var valor = input.value;


    if (valor !== lastSelectedItem) {
        var datalist = document.getElementById('product-selection');
        var options = datalist.options;
        var exists = false;
        

        for (var i = 0; i < options.length; i++) {
            
            if (valor == options[i].value) {
                exists = true;
                break;
            }
        }

        if (!exists) {
            input.value = '';
            input.placeholder = 'Producto no existe';
            
        }
    }
    else {
        lastSelectedItem = null;
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
}

