import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import language
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_firebase_credentials():
    # Use environment variables for sensitive information
    url = "https://firebasestorage.googleapis.com/v0/b/lookflock-api.appspot.com/o/serviceAccountKey.json?alt=media&token=1899423d-ce09-412c-b508-4ffa333d06ed"
    response = requests.get(url)
    if response.status_code == 200:
        key_dict = json.loads(response.text)  
        return credentials.Certificate(key_dict)
    else:
        raise Exception(f"Failed to retrieve Firebase credentials: {response.status_code}")

try:
    cred = get_firebase_credentials()
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Initialize the Google Cloud client with the same credentials if possible
    # client = language_v1.LanguageServiceClient(credentials=cred)
    client = language.LanguageServiceClient(credentials=cred)
except Exception as e:
    print(f"Error initializing services: {e}")
    raise

@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting."""
    return "Hello World!"

@app.route('/getTextEvaluation/<text>', methods=['GET'])
def text_evaluation(text):
   
    if not text:
        return jsonify({"error": "No text provided"}), 400
    print(text)
    try:
        # Prepare the document with the input text
        document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
        )
        print(client.moderate_text(document=document))
        # Detects the sentiment of the text
        # sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

        # Format the response data
        # # print(f"Text: {text}")
        # print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")
        # result = {'score': sentiment.score, 'magnitude': sentiment.magnitude}
        # return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)