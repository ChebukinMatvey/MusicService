const { remote, app, BrowserWindow, ipcMain } = require('electron')


require('electron-reload')(__dirname, {
    electron: require(`${__dirname}/node_modules/electron`)
})
var win

function createWindow(filename) {
    win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        }
    })
    win.loadFile('./html/login.html')
    // win.on('closed', () => {win = null})
}


app.on('ready', createWindow)

ipcMain.on('logined', (e, a) => {
    nwin = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        }
    })
    nwin.loadFile('./html/template.html')
    win.close()
    win = nwin
    win.webContents.on('did-finish-load',()=>{
        win.webContents.send('save-username', a)
    })
})