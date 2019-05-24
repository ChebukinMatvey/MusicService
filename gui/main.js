const { app, BrowserWindow } = require('electron')
require('electron-reload')(__dirname,{
    electron: require(`${__dirname}/node_modules/electron`)
})

let win

function createWindow() {
    win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        }
    })
    // win.setResizable(false)
    win.loadFile('./html/index.html')
    win.webContents.openDevTools()
    win.on('closed', () => {
        win = null
    })
}

app.on('ready', createWindow)