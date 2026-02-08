const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    send: (channel, data) => {
        let validChannels = ['to-python'];
        if (validChannels.includes(channel)) {
            ipcRenderer.send(channel, data);
        }
    },
    onResponse: (callback) => ipcRenderer.on('from-python', (event, value) => callback(value))
});
