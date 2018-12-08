function speechToText(data, callback) {
    let formData = new FormData();
    formData.append('file', new File([data], "speech"));

    reqwest({
        url: '/api/speech_recognition',
        method: 'post',
        processData: false,
        data: formData
    }).then(response => {
        callback(response);
    });
}

function addBubble(clazz, html) {
    let newBubble = document.createElement("p");
    newBubble.className = clazz;
    newBubble.innerHTML = html;
    document.getElementById("rightPanel").appendChild(newBubble);
}

function changeLastBubbleHTML(html) {
    document.getElementById("rightPanel").lastChild.innerText = html;
}

function deleteLastBubble() {
    let panel = document.getElementById("rightPanel");
    panel.removeChild(panel.lastChild);
}
