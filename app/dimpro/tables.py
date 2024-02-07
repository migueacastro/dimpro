from .models import User, Product, Order

def order_table(n=None, p=None):
    if p == 1:
        if n:
            orders = Order.objects.filter(status='pendiente')[:n]
        else:
            orders = Order.objects.filter(status='pendiente')
    elif p == 2: 
        if n:
            orders = Order.objects.filter(status='preparado')[:n]
        else:
            orders = Order.objects.filter(status='preparado')
    else:    
        if n:
            orders = Order.objects.all()[:n]
        else:
            orders = Order.objects.all()

    list_of_orders = []
    for order in orders:
        op = int(order.product_id.id)
        product = Product.objects.get(id=op)
        user = User.objects.get(email=order.user_email)
        order_dict = {
            'order_id': int(order.id), 
            'product_name': product.item,
            'user_name': f'{user.name} {user.last_name}',
            'email': user.email,
            'quantity': order.quantity,
            'status': order.status.capitalize(),
            'date': order.date
        }
        list_of_orders.append(order_dict)
    return list_of_orders

def client_table():
    
        
    clients = User.objects.filter(is_superuser=False,is_staff=False)

    list_of_orders = []
    for client in clients:
        orders = Order.objects.filter(user_email=client.id).count()
        client_dict = {
            'id': client.id, 
            'name': client.name,
            'last_name': client.last_name,
            'email': client.email,
            'date_joined': client.date_joined,
            'last_login': client.last_login,
            'order_count': orders
        }
        list_of_orders.append(client_dict)
    return list_of_orders

def client_orders_table(id):
    
    orders = Order.objects.filter(user_email=id)

    list_of_orders = []
    for order in orders:
        op = int(order.product_id.id)
        product = Product.objects.get(id=op)
        order_dict = {
            'order_id': int(order.id), 
            'product_name': product.item,
            'quantity': order.quantity,
            'status': order.status.capitalize(),
            'date': order.date
        }
        list_of_orders.append(order_dict)
    return list_of_orders