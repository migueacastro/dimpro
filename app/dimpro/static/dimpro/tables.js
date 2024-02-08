let dataTable;
let dataTableIsInitialized=false;

function ShowDataTable (dataTableModel) {
    const initDataTable=async()=>{
        if(dataTableIsInitialized){
            dataTable.destroy();
        }
        await dataTableModel();
        dataTable = $('#datatable-orders').DataTable({
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
        const response=await fetch('/app/list_orders/');
        const data= await response.json();

        let content=``;
        data.orders.forEach((order, index)=>{
            content+=`
                <tr class="clickable-row" data-href="http://127.0.0.1:8000/app/staff/view/order/${order.id}">
                    <td>${order.id}</td>
                    <td>${order.user_email}</td>
                    <td>${order.client_name}</td>
                    <td>${order.products}</td>
                    <td><p class="red-bg rounded text-center second-text grow w-auto">${order.status}</p></td>
                    <td>${order.date}</td>
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