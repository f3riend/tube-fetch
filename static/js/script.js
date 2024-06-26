let fiomat = document.getElementById('fiomat');
let info = document.getElementById('info');
let link = document.getElementById("link");

let filetype = false;

fiomat.addEventListener('change', (e) => {
    let state = e.target.checked;
    if (state) {
        info.innerText = 'Download type switched to mp3';
        info.classList.add('active');
        filetype =  true;
    } else {
        info.innerText = 'Download type switched to mp4';
        info.classList.remove('active');
        filetype = false;
    }
});

var socket = io();
var btn = document.getElementById('myButton');

btn.addEventListener('click', function (event) {
    event.preventDefault();
    socket.emit('download',filetype);
});

socket.on('downloaded', function() {
    alert('Downloaded event received.');
});
