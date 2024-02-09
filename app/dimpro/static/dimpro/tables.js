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
            actions = `
            <a onclick="editItem()">
                <i class="fa-solid fa-pen-to-square text-warning mx-1"></i>
            </a>
            <a onclick="editItem()">
                <i class="fa-solid fa-x text-danger mx-1"></i>
            </a>
            `
            content+=`
            <tr id="${index}">
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.reference}</td>
                <td>${product.quantity}</td>
                <td>${actions}</td> 
            </tr>
            `;
            
        });
        tableBody_orders.innerHTML=content;
    } catch(ex) {
        alert(ex);
    }
};
