const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  // 暂时加载一个简单的提示，后续你可以接入 Next.js 界面
  win.loadURL('data:text/html,<h1>Deep Focus Core v1.1.0</h1><p>L-A-T-T Protocol Active.</p>');
}

app.whenReady().then(createWindow);
