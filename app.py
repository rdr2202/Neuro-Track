from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import pyttsx3
from threading import Thread
import webbrowser
from gtts import gTTS
import openai
import uuid  # Import UUID module to generate unique filenames

app = Flask(__name__)

engine = pyttsx3.init()

openai.api_key = "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"

def ask_question(question, temperature=0.5):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Your Name is Neuraa, and you are a Friendly Psychiatrist, You are good at emotional and sentiment analysis and offer solutions for emotional and mental health issues"
            },
            {
                "role": "user",
                "content": question
            },
           
        ],
        temperature=temperature
    )
    return response.choices[0].message["content"]

def synthesize_speech(text, output_file):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en', slow=False)
    # Save the audio file with a unique filename
    tts.save(output_file)

def generate_response(question):
    response_text = ask_question(question, temperature=0.5)
    audio_filename = f'static/response_{uuid.uuid4()}.mp3'  # Generate a unique filename for the audio response
    synthesize_speech(response_text, audio_filename)
    return response_text, audio_filename

@app.route('/')
def index():
    return render_template('index_combined.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['msg']
    response_text, audio_filename = generate_response(user_message)
    return jsonify({'response': response_text, 'audio': audio_filename})

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('static', filename)

def run_flask_app():
    app.run(host='127.0.0.1', port=5004, debug=False, threaded=True)

def open_browser():
    import time
    time.sleep(2)  # Delay to ensure Flask server has started
    webbrowser.open_new_tab("http://localhost:5004/")

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    open_browser()

