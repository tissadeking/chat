URL = window.URL || window.webkitURL;
var gumStream;
var recorder;
var input;
var encodingType;
var encodeAfterRecord = true;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext;
//var encodingTypeSelect = document.getElementById("encodingTypeSelect");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add event listeners
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);


//to add response to the chat
function sendMessage() {
    const user_input = document.getElementById('user_input').value;
    if (user_input.trim() !== "") {
        appendMessage('user', user_input);
        document.getElementById('user_input').value = ''; // clear input field
        document.getElementById('user_input').focus(); // focus back on input

        fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `user_input=${user_input}`
        })
        .then(response => response.text())
        .then(data => {
            //document.getElementById('response').innerText = data;
            //document.getElementById('response').innerHTML = data;
            appendMessage('bot', data);
        });
    }
}

//function to append message to the chat box
function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);
    messageElement.innerHTML = `<div class="message-text">${message}</div>`;
    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}

//generate a response when user starts
function generateBotResponse(userMessage) {
    const lowerCaseMessage = userMessage.toLowerCase();

    if (lowerCaseMessage.includes('hello') || lowerCaseMessage.includes('hi')) {
        return 'Hello! How can I help you today?';
    } else if (lowerCaseMessage.includes('bye')) {
        return 'Goodbye! Have a great day!';
    } else {
        return 'Can you proceed with your intent or query?';
    }
}

//function to allow user to press Enter to send the message
document.getElementById('user_input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});



//function to start recording
function startRecording() {
    console.log("startRecording() called");

    var constraints = { audio: true, video: false };

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("Microphone access granted, initializing recorder...");

        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        //encodingType = encodingTypeSelect.value;
        //encodingTypeSelect.disabled = true;
        encodingType = "wav";

        recorder = new WebAudioRecorder(input, {
            workerDir: "static/js/",
            encoding: encodingType,
            numChannels: 1, // Mono recording
            onEncoderLoading: function() { console.log("Loading encoder..."); },
            onEncoderLoaded: function() { console.log("Encoder loaded"); }
        });

        recorder.onComplete = function(_, blob) {
            console.log("Recording complete, sending for transcription...");
            sendAudioToServer(blob);
        };

        recorder.setOptions({ timeLimit: 120, encodeAfterRecord: encodeAfterRecord });

        recorder.startRecording();
        console.log("Recording started");

    }).catch(function(err) {
        console.error("Error accessing microphone:", err);
    });

    recordButton.disabled = true;
    stopButton.disabled = false;
}

//function to stop recording
function stopRecording() {
    console.log("stopRecording() called");

    gumStream.getAudioTracks()[0].stop();
    stopButton.disabled = true;
    recordButton.disabled = false;

    recorder.finishRecording();
    console.log("Recording stopped");
}

//FOR VOICE NOTE
function sendAudioToServer(blob) {
    var formData = new FormData();
    formData.append("audio", blob, "recording.wav");

    fetch("/transcribe", {
    //fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        appendMessage('bot', data.transcription);
        //console.log("Transcription received:", data.transcription);
        //document.getElementById("speechText").innerText = data.transcription;
        // Decode and play the response audio
        /*if (data.audio) {
            let audio = new Audio("data:audio/wav;base64," + data.audio);
            audio.play();
        }*/
    })
    .catch(error => {
        console.error("Error transcribing audio:", error);
    });
}

