var resultimg = document.getElementById("resultimg")
var suspectlistitem = document.getElementById('Suspectlistitem');
var suspectlist_names = [];
var newsuspects = ''

//var result = document.getElementById("result");
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var mode = true;

var ws = new WebSocket(    ws_scheme + ${window.location.host}+'/FR/'   );


function ResultFaceRecognition(SuspectList) {
    let newsuspect = '';
    for (let item of SuspectList) {
        if (!suspectlist_names.includes(item)) {
            suspectlist_names.push(item);
            newsuspect = item;
        }
    }
    return  suspectlist_names,newsuspect;
}

    ws.onopen = (event) => {
       console.log('Client Side Face recognition Web Connection Established');};

    ws.onmessage = (event) => {

       console.log("Recieved from Face Recognition Connection");
       recdata = JSON.parse(event.data);
       console.log(recdata)
       frameUpdate = recdata.frame;
       resultimg.src = "data:image/jpeg;base64," + frameUpdate;

       suspectlist = recdata.suspectlist;
       console.log(suspectlist)
       console.log(recdata.suspectdatalist);
       suspectlist_names,newsuspects = ResultFaceRecognition(suspectlist)
       console.log( "This is the suspect list" + suspectlist_names)
       console.log("This is the new  suspect" +newsuspects)



       if (newsuspects != '')
       {
           const newItem = document.createElement('li');
           newItem.innerHTML = `
            <img class="suspimg" src=${recdata.suspectdatalist[0].Image_url}>
            <B>Full Name:</B>${recdata.suspectdatalist[0].First_name}<br>
            <B>Age:</B> ${recdata.suspectdatalist[0].Age}<br>
            <B>Idetifying Features:</B> ${recdata.suspectdatalist[0].Identifying_features}<br>
            <B>Criminal History:</B> ${recdata.suspectdatalist[0].Criminal_History}<br>
            <B>Behavioral Patterns:</B> ${recdata.suspectdatalist[0].Behavioral_Patterns}<br>
            `;
            suspectlistitem.appendChild(newItem);

       }


       };



    ws.onclose = (event) => {
       console.log('Client Side Face recognition Web Connection Disconnected');};











