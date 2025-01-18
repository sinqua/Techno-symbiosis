from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import llm
import base64

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/send', methods=['POST'])
def hello_send():
    text = request.form.get('text')
    image = request.files.get('image')
    user_input = None
    encoded_image = None

    if text:
        print ("You said: ", text)
        user_input = text
    if image:
        print ("You sent an image")
        image_data = image.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

    message = llm.chat_ai(user_input, encoded_image)
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)