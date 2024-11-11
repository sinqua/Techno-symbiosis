import time
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import easyocr
import llm

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
    print("I received an image")
    image = request.files['image']
    image = image.read()
    result = reader.readtext(image, detail=0)
    user_input = ' '.join(result)
    print("Read your letter")


    print("Ask to llama")
    message = llm.chat_ai(user_input)
    print("I got the answer")
    return  message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)