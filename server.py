from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import easyocr
import llm
from datetime import datetime

reader = easyocr.Reader(['ko', 'en'], gpu=True)

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/text', methods=['POST'])
def hello_text():
    print("I received an text")
    text = request.form['text']

    user_input = text
    print("Ask to llama")
    message = llm.chat_ai(user_input)

    return message

@app.route('/image', methods=['POST'])
def hello_image():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"I received an image at {current_time}")
    image = request.files['image']
    image = image.read()
    result = reader.readtext(image, detail=0)
    user_input = ' '.join(result)
    print("Read your letter")


    print("Ask to llama")
    message = llm.chat_ai(user_input)
    print("I got the answer")
    return  message

@app.route('/voice', methods=['POST'])
def hello_voice():
    print("I received an voice")
    voice = request.form['voice']

    user_input = voice
    print("Ask to llama")
    message = llm.chat_ai(user_input)

    return message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)