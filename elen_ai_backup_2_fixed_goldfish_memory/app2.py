from flask import Flask, request, render_template, jsonify

#from flask import Flask, request, render_template
import openai 
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
#import config
from config import OPENAI_API_KEY
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity

from chat import get_response

openai.api_key = OPENAI_API_KEY


app = Flask(__name__)

@app.get("/")
def index_get():
	return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True) 