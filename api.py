from flask import Flask, send_file, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'


@app.route('/image/<path:url>.jpg') # simple server to proxy images from google photos to freeimage.host
def serve_image(url):
    # Send a request to the remote URL to get the image data
    response = requests.get(url)

    # Set the Content-Disposition header to attachment
    headers = {'Content-Disposition': 'attachment'}

    # Return the response to the client
    return Response(response.content, headers=headers, mimetype=response.headers['Content-Type'])    # Set the Content-Disposition header to attachment


if __name__ == '__main__':
    app.run()
