const {ipcRenderer} = require('electron')

btn = document.getElementById("btnLogin")
btn.addEventListener('click',()=>{
    login()
})

function login(){
    ipcRenderer.send('logined','nokinobi')
}



