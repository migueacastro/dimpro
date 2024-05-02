


async function pushForm () {

    const head = 'DIMPRO';
    const body = 'Has recibido un nuevo pedido';
    const meta = document.querySelector('meta[name="user_id"]');
    const id = meta ? meta.content : null;

    // TODO: make an AJAX request to send notification
    if (head && body && id) {
        const res = await fetch('/send_push', {
            method: 'POST',
            body: JSON.stringify({head, body, id}),
            headers: {
                'content-type': 'application/json'
            }
        });
        if (!(res.status === 200)) {
            console.log('Something broke..  Try again?');
        }
    }
    else {
        let error;
        if (!head || !body){
            error = 'Please ensure you complete the form'
        }
        else if (!id){
            error = "Are you sure you're logged in?. Make sure!"
        }
        console.log(error);
    }
};