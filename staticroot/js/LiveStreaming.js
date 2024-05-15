var livestreamingimg = document.getElementById("livestreamingimg")
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var mode = true;


var ws = new WebSocket( ws_scheme + '://192.168.1.8:8000/LS/' );

    ws.onopen = (event) => {
       console.log('Client Side Live Streaming Web Connection Established');};

    ws.onmessage = (event) => {
       console.log("Recieved from Live Streaming Connection");
       frame = event.data;
       livestreamingimg.src = "data:image/jpeg;base64," + frame;};

    ws.onclose = (event) => {
       console.log('Client Side Live Streaming Web Connection Disconnected');};










