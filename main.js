const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200, height: 900, title: "L-A-T-T | OPENCLAW AGENT",
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true
        }
    });

    win.loadFile('src/index.html');

    // 使用 -u 参数强制 Python 不使用缓存
    const pyPath = path.join(__dirname, 'core_v1_1.py');
    const pythonProcess = spawn('python3', ['-u', pyPath]);

    ipcMain.on('to-python', (event, arg) => {
        console.log('--- 物理层发送 ---:', arg);
        pythonProcess.stdin.write(arg + "\n");
    });

    pythonProcess.stdout.on('data', (data) => {
        const str = data.toString();
        console.log('--- 物理层接收 ---:', str);
        win.webContents.send('from-python', str);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error('Python 错误:', data.toString());
        win.webContents.send('from-python', "SYSTEM ERR: " + data.toString());
    });
}

app.whenReady().then(createWindow);
