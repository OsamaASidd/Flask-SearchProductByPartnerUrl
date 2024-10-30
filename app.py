import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from algoliasearch.search_client import SearchClient
app = Flask(__name__)

# Initialize Algolia client
ALGOLIA_APP_ID = 'EMFUSB67CG'
ALGOLIA_API_KEY = '0f7466afc30b24c667a61b43cf879898'
ALGOLIA_INDEX_NAME = 'products'

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)


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
except Exception as e:
    print(f"Error initializing services: {e}")
    raise

@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting."""
    return "Hello World!"

@app.route('/searchProduct', methods=['GET'])
async def search_product():
        try:
        # Get query parameters from request
            query = request.args.get('query', '')
            page = int(request.args.get('page', 0))  # Get page number (default 0)
            hits_per_page = int(request.args.get('hitsPerPage', 1))  # Default 9 results per page

            if len(query) < 3:
                return jsonify({"error": "Search query must be at least 3 characters"}), 400

            search_result =  index.search(query, {
                'attributesToRetrieve': [
                    'objectID',
                    'name',
                    'subSubCategory',
                    'imageUrl'
                ],
                'hitsPerPage': hits_per_page
            })

            return jsonify(search_result), 200


        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)