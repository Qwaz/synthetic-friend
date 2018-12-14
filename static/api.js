function speechToText(data, callback, failure) {
    let formData = new FormData();
    formData.append('file', new File([data], "speech"));
    console.log("Trying to recognize speech...");

    reqwest({
        url: '/api/speech_recognition',
        method: 'post',
        data: formData,
        processData: false
    }).then(response => {
        callback(response);
    }, error => {
        if (failure) {
            failure(error);
        }
    });
}

function generateResponse(data, callback, failure) {
    console.log("Generating response for: " + data);
    reqwest({
        url: '/api/response_generation',
        method: 'post',
        data: {
            text: data
        }
    }).then(response => {
        console.log("Response for '" + data + "' is: " + response);
        callback(response);
    }, error => {
        if (failure) {
            failure(error);
        }
    });
}

function generateSpeech(data, callback, failure) {
    console.log("Generating speech for: " + data);
    reqwest({
        url: '/api/speech_generation',
        method: 'post',
        data: {
            text: data
        }
    }).then(response => {
        console.log("Generated speech is at: " + response.audio);
        callback(response);
    }, error => {
        if (failure) {
            failure(error);
        }
    });
}

function addBubble(clazz, html) {
    let newBubble = document.createElement("p");
    newBubble.className = clazz;
    newBubble.innerHTML = html;
    let panel = document.getElementById("rightPanel");
    panel.appendChild(newBubble);
    panel.scrollTop = panel.scrollHeight;
}

function changeLastBubbleHTML(html) {
    document.getElementById("rightPanel").lastChild.innerText = html;
}

function deleteLastBubble() {
    let panel = document.getElementById("rightPanel");
    panel.removeChild(panel.lastChild);
}
