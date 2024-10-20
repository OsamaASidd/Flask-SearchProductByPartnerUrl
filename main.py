import os
import json
import requests
from google.cloud import language
import google.generativeai as genai

GOOGLE_API_KEY="AIzaSyDLALmBwgf7xcEu5mY3pS6JL_FsN85LTxw"
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if __name__ == '__main__':
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # """Generates suggestions to rewrite the text using generative AI."""
    prompt = """
    Determine if it is inappropriate or negative or has sexual explicit or has hate speech or harassment or dangerous content.
     If so respond with "Inappropriate or negative.",  If the Text is acceptable as it is, simply respond with "No modification needed."
    Text: "{text}"
    """

    text_to_check = "This product is the best!"

    response = model.generate_content(prompt.format(text=text_to_check))

    print(response)