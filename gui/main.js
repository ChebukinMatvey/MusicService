const {app,BrowserWindow} = require('electron')

var win 

app.on('ready',()=>{
    win = new BrowserWindow({
        width:500,
        height:300
    })
    win.loadFile('./index.html')
})


