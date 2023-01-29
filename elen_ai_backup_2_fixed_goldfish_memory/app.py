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

from chat import open_file, get_response, get_convo

openai.api_key = OPENAI_API_KEY


app = Flask(__name__)
conversation = list()


@app.get("/")
def index_get():
	return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = get_response(text)
    message = {"message": response}
    return jsonify(message)


@app.post("/speak")
def speak():
    
    f = open("promptsave.txt","w+")    
    while True:    
        user_message = request.get_json().get("message")
        conversation.append('Customer: ' + user_message)
            
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nELEN:'
            
        response = get_convo(prompt)

        print('2. ELEN:', response)
        conversation.append('ELEN: %s' % response)
            
            ###

        f.write(prompt)
         
            ###

        message = {"answer": response} 
        return jsonify(message)        
    f.close()   

    

if __name__ == '__main__':

    app.run(debug=True)    

"""#
from flask import Flask, request, render_template
import openai 
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
#import config
from config import OPENAI_API_KEY
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity


openai.api_key = OPENAI_API_KEY

app = Flask(__name__)



@app.route('/')
def search_form():
  return render_template('search_form.html')

@app.route('/search')
def search():
    # Get the search query from the URL query string
    query = request.args.get('query')

    search_term_vector = get_embedding(query, engine="text-embedding-ada-002")

    df = pd.read_csv('earnings-embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))

    sorted_by_similarity = df.sort_values("similarities", ascending=False).head(3)
    results = sorted_by_similarity['text'].values.tolist()

#    results = [item for item in items if query in item]
    # Render the search results template, passing in the search query and results
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
  app.run()



"""