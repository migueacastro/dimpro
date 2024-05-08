let dataTable;
let dataTableIsInitialized = false;


function getUrlId() {
    url = window.location.href;
    lastitem = url.split('/').filter(Boolean).pop();
    if (isNaN(lastitem)) {
        return false;
    }
    return lastitem;
}
var IdUrl = getUrlId();

function ShowDataTable(dataTableModel) {
    const initDataTable = async () => {
        if (dataTableIsInitialized) {
            dataTable.destroy();
        }
        await dataTableModel();
        dataTable = $('#datatable-orders').DataTable({
            "retrieve": true,
            "iDisplayLength": -1,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible",
                "sInfo": "",
                "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast": "Último",
                    "sNext": "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            },
            
        });

        dataTableIsInitialized = true;
    };

    window.addEventListener('load', async () => {
        await initDataTable();
        
    });
}

function editDataTable(dataTableModel) {
    const initDataTable = async () => {
        if (dataTableIsInitialized) {
            dataTable.destroy();
        }
        await dataTableModel();
        dataTable = $('#datatable-orders').DataTable({
            "paging": false,
            "iDisplayLength": -1,
            "searching": false,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "",
                "sInfoEmpty": "  ",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast": "Último",
                    "sNext": "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            }
        });

        dataTableIsInitialized = true;
    };

    window.addEventListener('load', async () => {
        await initDataTable();
        window.addEventListener("keydown", function (e) {
            if (13 == e.keyCode) { 
                e.preventDefault();
                addRow();
            } 
        });
    });
}


const listOrders = async () => {
    try {

        let response;
        let url = window.location.href;

        if (url.includes("/client/orders/") || url.includes("/staff/view/seller/")) {
            response = await fetch(`/list_orders/user/${IdUrl}/`);
        }
        else if (url.includes("/staff/dashboard/")) {
            response = await fetch(`/list_orders/`);
        }
        else {
            response = await fetch('/list_orders/all/');
        }

        const data = await response.json();

        let content = ``;
        data.orders.reverse().forEach((order, index) => {
            if (IdUrl || order.products > 0) {
                if (checkUser()) {
                    content += `
                <tr class="clickable-row" data-href="/client/order/view/${order.id}/">
                    <td>${order.id}</td>`;
                }
                else {
                    content += `
                <tr class="clickable-row" data-href="/staff/view/order/${order.id}/">
                    <td>${order.id}</td>`;
                }
                if (!(window.location.href.includes("/client/orders/"))) {
                    content += `<td>${order.user_email}</td>`;
                }
                content += `
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
        tableBody_orders.innerHTML = content;
        try {
            $('#datatable-orders').DataTable().order([[5, 'desc']]).draw();
        }
        catch (error) {
            $('#datatable-orders').DataTable().order([[4, 'asc']]).draw();
        }
    } 
    catch (ex) {
        console.log(ex);
        
    }
};


const listOrdersAll = async () => {
    try {
        let response;
        response = await fetch('/list_orders/all/');


        const data = await response.json();
        let content = ``;
        data.orders.reverse().forEach((order, index) => {
            if (order.products > 0) {
                content += `
                <tr class="clickable-row" data-href="/staff/view/order/${order.id}/">
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
        tableBody_orders.innerHTML = content;
        $('#datatable-orders').DataTable().order([[5, 'desc']]).draw();
    } catch (ex) {
        alert(ex);
    }
};

const listSellers = async () => {
    try {
        const response = await fetch('/list_sellers/');
        const data = await response.json();

        let content = ``;
        data.sellers.forEach((user, index) => {
            content += `
                <tr class="clickable-row" data-href="/staff/view/seller/${user.id}/">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.orders}</td>
                    <td>${user.phonenumber}</td>     
            `;
            let isOperator = document.body.dataset.isOperator === 'True';
            if (isOperator) {
                content += `
                    <td><a class="primary-text" href="/staff/delete/${user.id}">
                    <i class="fa-solid fa-trash-can"></i>
                    </a></td>`;
            }
            content += `</tr>`;
        });
        tableBody_orders.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

const listEmployees = async () => {
    try {
        const response = await fetch('/list_employees/');
        const data = await response.json();

        let content = ``;
        data.employees.forEach((user, index) => {
            content += `
                <tr class="clickable-row" data-href="/staff/view/seller/${user.id}/">
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.phonenumber}</td>
                    <td><a class="primary-text" href="/staff/delete/${user.id}">
                    <i class="fa-solid fa-trash-can"></i>
                    </a></td>
                </tr>
            `;
        });
        tableBody_orders.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

$(document).ready(function ($) {
    $(document).on('click', '.clickable-row', function () {
        window.location.replace($(this).data("href"));
    });
});

const listOrderProducts = async () => {
    try {
        let response;
        response = await fetch(`/list_products_order/order/${IdUrl}/`);
        const data = await response.json();

        let content = ``;
        data.products.forEach((product, index) => {
            content += `
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
        tableBody_orders.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

var product_data;

const listOrderProductsEdit = async () => {
    try {
        let response;
        document.getElementById('total').innerText = document.getElementById('total-tosubmit').value + '$';
        let product_search = await fetch("/list_products/");


        response = await fetch(`/list_products_order/order/${IdUrl}/`);
        product_data = await product_search.json();
        const data = await response.json();

        let content = ``;
        data.products.forEach((product, index) => {
            let id;
            let reference;
            let availability;
            let item_name;
            product_data.products.forEach((item) => {
                if (item.id == product.id) {
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


            content += `
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
                <td id="cost-${index}">${(parseDollar(product.price * product.quantity))}$</td>
                <td><i class="fa-solid fa-xmark grow" onclick="deleteRow(${index});"></i></td>
            </tr>
            `;





        });
        tableBody_orders.innerHTML = content;
    } catch (ex) {
        console.log(ex);
    }
    updatePrices();
    updateTotal();

};
var product_data;
var inputId;
var lastSelectedItem;
function setInputValue(input, product_data) {
  inputId = input;
  var inputElement = document.getElementById(inputId);
  var id = getId(inputElement.id);
  var valor = inputElement.value;
  var rows = Array.from(document.getElementById('datatable-orders').rows);
  var itemCounts = {};
  var productExists = false;

  rows.forEach(row => {
    if (row.id) {
      var item = document.getElementById('item-' + row.id).value;
      itemCounts[item] = (itemCounts[item] || 0) + 1;

      if (valor === item && itemCounts[item] > 1) {
        console.log('El producto ya existe en la tabla');
        productExists = true;
      }
    }
  });

  if (productExists) {
    inputElement.value = '';
    inputElement.placeholder = 'El producto ya existe en la tabla';
  } else {
    lastSelectedItem = inputElement.value;
  }
}

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





async function changeValues(id, reference, aq, q, name, price, cost) {
    let value = document.getElementById(name).value;
    let product_id = $(`#product-selection option[value="${value}"]`).text();
    if (!product_id || product_id.trim() == "") {
        verify()
        return;
    }
    let v1 = "";
    let v2 = "";
    let v3 = "";
    let v4 = "";
    let v5 = "";
    let response = await fetch(`/getproduct/${product_id}/`);
    let product = await response.json();

    v1 = product.id;
    v2 = product.reference;
    v3 = product['available_quantity'];
    v4 = 1;
    let priceType = $('#select-ptype option:selected').text();
    Object.values(product.prices).forEach((dict) => {
        if (Object.keys(dict)[0] == priceType) {
            v5 = Object.values(dict)[0];
            
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
    updatePrices();
    updateTotal();
}

async function changeNumbers(id, q, price, cost) {


    
    input = document.getElementById(id);
    input.addEventListener('keyup', function () {
        let v4 = document.getElementById(q).value;
        let v5 = document.getElementById(price).innerText;
        let v6 = (parseDollar(v5) * parseDollar(v4));
        if (isNaN(v6)) {
            document.getElementById(cost).innerText = '';
        }
        else {
            document.getElementById(cost).innerText = parseDollar(v6) + '$';
        }

        updateTotal();
    })

    input.addEventListener('input', function () {
        let v4 = document.getElementById(q).value;
        let v5 = document.getElementById(price).innerText;
        let v6 = (parseDollar(v5) * parseDollar(v4));
        if (isNaN(v6)) {
            document.getElementById(cost).innerText = '';
        }
        else {
            document.getElementById(cost).innerText = parseDollar(v6) + '$';
        }

        updateTotal();
    })
    input.addEventListener('change', function () {
        let v4 = document.getElementById(q).value;
        let v5 = document.getElementById(price).innerText;
        let v6 = (parseDollar(v5) * parseDollar(v4));
        if (isNaN(v6)) {
            document.getElementById(cost).innerText = '';
        }
        else {
            document.getElementById(cost).innerText = parseDollar(v6) + '$';
        }

        updateTotal();
    })
}

function parseDollar(n) {
    return (parseFloat(n.toString().replace(/\$/, '')).toFixed(2));
}


async function updatePrices() {
    let pricetype = document.getElementById('select-ptype').value;

    // Change pricetype to submit
    document.getElementById('price-tosubmit').value = $('#select-ptype option:selected').text();
    let priceType = $('#select-ptype option:selected').text();
    let table = document.getElementById('tableBody_orders');
    let response = await fetch("/list_products/");
    let product_search = await response.json();

    // TODO
    Array.from(table.rows).forEach(row => {
        if (row.id) {
            let index = row.id;
            product_search.products.forEach((product) => {
                if (product.reference == document.getElementById('reference-' + index).innerText) {

                    Object.values(product.prices).forEach((dict) => {
                        if (Object.keys(dict)[0] == priceType) {
                            price = Object.values(dict)[0];
                        } 
                    });

                    price = parseDollar(price);
                    document.getElementById('price-' + index).innerText = price + '$';
                    
                    let quantity = document.getElementById('item-q-' + index).value;
                    let cost = parseDollar(price * parseFloat(quantity));
                    document.getElementById('cost-' + index).innerText = cost + '$';
                }
            });
        }
    });
    updateTotal();
}
function updateTotal() {
    
    let table = document.getElementById('tableBody_orders');
    let total = 0;
    for (let i = 0; i < table.rows.length; i++) {
        if (!document.getElementById(i)) {
            continue;
        }
        if (document.getElementById(i).style.display === 'none') {
            if (document.getElementById('cost-d-' + i)) {
                numbertosum = -(parseFloat(parseDollar(document.getElementById('cost-d-' + i).innerText)));
            }
            continue;
        }
        else {
            numbertosum = parseFloat(parseDollar(document.getElementById('cost-' + i).innerText));
        }

        if (isNaN(numbertosum)) {
            continue;
        }
        total = parseFloat(total) + numbertosum;
        
    };

    let iva = parseDollar(total * 16 / 100);
    let subtotal = parseDollar(total);
    let indexOptions = document.getElementById('select-ptype');

    // Detal O Base posee IVA
    if (indexOptions.options[indexOptions.selectedIndex].text == 'Detal o Base') {
        
        // Con IVA
        total = parseDollar(parseFloat(total) + parseFloat(iva));
        document.getElementById('iva').setAttribute('class', 'd-flex flex-row align-items-center justify-content-end')
        document.getElementById('iva-v').innerText = `${iva}$`;
        document.getElementById('subtotal').setAttribute('class', 'd-flex flex-row align-items-center justify-content-end');
        document.getElementById('subtotal-v').innerText = `${subtotal}$`;
    }
    else {

        // Sin IVA
        document.getElementById('iva').setAttribute('class', 'd-none flex-row align-items-center justify-content-end');
        document.getElementById('subtotal').setAttribute('class', 'd-none flex-row align-items-center justify-content-end');
    }
    document.getElementById('total-tosubmit').value = parseDollar(total);
    document.getElementById('total').innerText = parseDollar(total) + '$';
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
    input1.onchange = function () {
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
    input2.onfocus = function () {
        changeNumbers('item-q-' + index, 'item-q-' + index, 'price-' + index, 'cost-' + index);
    }
    let icon = document.createElement('i');
    icon.className = 'fa-solid fa-xmark';
    icon.onclick = function () {
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


function deleteRow(id) {
    $(`#${id}`).remove();
    let rowId = parseInt(id);
    let rows = $('#tableBody_orders tr');
    rows.each(function(index, row) {
    if (index < rowId) {
        return;
    } 
    if (row.id) {
        row.id = index;
        $(`#item-${index + 1}`).prop('id', `item-${index}`);
        $(`#id-${index + 1}`).prop('id', `id-${index}`);
        $(`#reference-${index + 1}`).prop('id', `reference-${index}`);
        $(`#aq-${index + 1}`).prop('id', `aq-${index}`);
        $(`#item-q-${index + 1}`).prop('id', `item-q-${index}`);
        $(`#price-${index + 1}`).prop('id', `price-${index}`);
        $(`#cost-${index + 1}`).prop('id', `cost-${index}`);
    }
});

    updateTotal();
}

function getId(str) {
    return str.split('/').filter(Boolean).pop();
}

function checkUser() {
    return window.location.href.includes('/client/');
}

function checkStaff() {
    return window.location.href.includes('/staff/');
}

function postData() {
    let table = document.getElementById('tableBody_orders');
    let data = [];

    Array.from(table.rows).forEach(row => {
        if (row.id) {
            let index = row.id;
            let item = document.getElementById('item-' + index).value;
            let reference = document.getElementById('reference-' + index).value;
            let quantity = document.getElementById('item-q-' + index).value;
            let cost = parseDollar(document.getElementById('cost-' + index).innerText);
            let price = parseDollar(document.getElementById('price-' + index).innerText);
            
            try {
                data.push({
                    item: item,
                    reference: reference,
                    cost: cost,
                    price: price,
                    quantity: quantity
                });
            }
            catch (error) {
                console.log(error);
                return;
            }

        }
    });

    if (url.includes('/client/')) {
        fetch(`/client/order/edit/${IdUrl}/`, {
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
        fetch(`/staff/view/order/edit/${IdUrl}/`, {
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

