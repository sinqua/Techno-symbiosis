import time
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import easyocr
import llm
from waitress import serve

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
    def gernerate():
        print("I received an image")
        image = request.files['image']
        image = image.read()

        print("Reading your letter")
        result = reader.readtext(image, detail=0)
        user_input = ' '.join(result)

        print("Ask to llama")

        for _ in range(30):
            yield " "
            time.sleep(1)

        message = llm.chat_ai(user_input)
        yield message

    return Response(stream_with_context(gernerate()))

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    serve(app, host='0.0.0.0', port=8080, channel_timeout=3600)