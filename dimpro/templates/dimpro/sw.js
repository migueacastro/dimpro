self.addEventListener('push', function (event) {
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification 🕺🕺';
    const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
    const url = 'https://app.dimproelect.com/'; // URL a abrir cuando se haga clic en la notificación
    
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: 'https://app.dimproelect.com/static/dimpro/favicon.jpg' ,
            data: {
                url: url, // Guardar la URL en los datos de la notificación
                
            },

            
        })
    );
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close(); // Cerrar la notificación
    event.waitUntil(
        clients.openWindow(event.notification.data.url) // Abrir la URL en una nueva pestaña
    );
});