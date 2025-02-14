import io
import pyttsx3
from flask import Flask, render_template, request, jsonify, send_file
from llm_user_preference import llm_preference_fun
from select_model import select_model_fun
from rate_models import rate_models_fun
from start_2_old import start_fun
import nltk, os, re, json, whisper, soundfile as sf
import speech_recognition as sr

nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
#)
rating_store = 'model_ratings.csv'
if (os.path.exists(rating_store) and os.path.isfile(rating_store)):
    os.remove(rating_store)
rate_models_fun()

use_case = 'GREEN DEAL'
app = Flask(__name__, static_folder="static")

def remove_unwanted_chars(text):
    return re.sub(r"[^a-zA-Z0-9.,:; ]", "", text)

to_query = 0

global csv_to_query

@app.route("/")
def home():
    return render_template("index.html")

#for chatting
@app.route("/get_response", methods=["POST"])
def get_response():
    #print('started')
    global to_query
    global csv_to_query
    user_input = request.form['user_input']

    if user_input == 'exit' or user_input == 'finish' or user_input == 'end':
        to_query = 0
    #response = chatbot.get_response(user_input)
    output = llm_preference_fun(user_input)
    if output['type'] == 'intent':
        selected_model = select_model_fun(output['result'])
        response = 'Intent Received. Selected Model is {0}. Proceed with your Query.'.format(selected_model)
    else:
        response = start_fun(user_input, use_case)

    return str(response)


#for continuous recording
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    print('Started transcription...')
    #transcription = ""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400
    file = request.files["audio"]

    audio_bytes = io.BytesIO(file.read())

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_bytes) as source:
        recognizer.adjust_for_ambient_noise(source)  #reduce background noise
        audio_data = recognizer.record(source)  #capture the entire audio
    try:
        transcription = recognizer.recognize_google(audio_data)
        print("Transcript:", transcription)
    except sr.UnknownValueError:
        transcription = "Sorry, could not understand the audio."
    except sr.RequestError:
        transcription = "Could not request results, please check your internet connection."

    #process the transcription with the LLM function
    output = llm_preference_fun(transcription)

    if output["type"] == "intent":
        selected_model = select_model_fun(output["result"])
        response = f"Intent Received. Selected Model is {selected_model}. Proceed with your Query."
    else:
        response = start_fun(transcription, use_case)

    return jsonify({"transcription": response})


if __name__ == "__main__":
    app.run(port=5002, debug=True)
    #socketio.run(app, port=5002, debug=True, allow_unsafe_werkzeug=True)
