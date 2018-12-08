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
