import { CapacitorNotifications } from '@capacitor/background-runner';

//:todo improve this code
addEventListener('myCustomEvent', (resolve) => {
    console.log('Executing background task...');
    // Perform background operations
    resolve(); // Call resolve when the task is complete
});

addEventListener('remoteNotification', (resolve, reject) => {
    try {
        console.log('Received silent push notification');
        CapacitorNotifications.schedule([
            {
                id: 100,
                title: 'Notification',
                body: 'Background task executed.',
            },
        ]);
        resolve();
    } catch (err) {
        reject(err);
    }
});