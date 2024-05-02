const registerSw = async () => {
    if ('serviceWorker' in navigator) {
        const reg = await navigator.serviceWorker.register('/sw.js');
        reg.update();
        initialiseState(reg)

    } else {
        console.log("You can't send push notifications ☹️")
    }
};

const initialiseState = (reg) => {
    if (!reg.showNotification) {
        console.log('Showing notifications isn\'t supported ☹️');
        return
    }
    if (Notification.permission === 'denied') {
        console.log('You prevented us from showing notifications ☹️');
        return
    }
    if (!'PushManager' in window) {
        console.log("Push isn't allowed in your browser");
        return
    }
    subscribe(reg);
}

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}

const subscribe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    if (subscription) {
        sendSubData(subscription);
        return;
    }

    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;
    const options = {
        userVisibleOnly: true,
        // if key exists, create applicationServerKey property
        ...(key && {applicationServerKey: urlB64ToUint8Array(key)})
    };

    const sub = await reg.pushManager.subscribe(options);
    sendSubData(sub)
};

const sendSubData = async (subscription) => {
    const user_agent = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident|chromium)/ig)[0].toLowerCase();
    const data = {
        status_type: 'subscribe',
        subscription: subscription.toJSON(),
        user_agent: user_agent,
        browser: user_agent,
    };

    const csrftoken = document.querySelector('meta[name="token"]');
    const token = csrftoken.content;

    const res = await fetch('/webpush/save_information', {
        method: 'POST',
        body: JSON.stringify(data),
        
        credentials: "include"
    });

    handleResponse(res);
};

const handleResponse = (res) => {
    console.log(res.status);
};

registerSw();