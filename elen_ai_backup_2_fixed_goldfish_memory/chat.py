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

#import random
#import json

#import torch

#from model import NeuralNet
#from nltk_utils import bag_of_words, tokenize

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#with open('intents.json', 'r') as json_data:
#    intents = json.load(json_data)

#FILE = "data.pth"
#data = torch.load(FILE)

#input_size = data["input_size"]
#hidden_size = data["hidden_size"]
#output_size = data["output_size"]
#all_words = data['all_words']
#tags = data['tags']
#model_state = data["model_state"]

#model = NeuralNet(input_size, hidden_size, output_size).to(device)
#model.load_state_dict(model_state)
#model.eval()


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def get_response(msg):
    
    #query = request.args.get('query')
    query = msg

    search_term_vector = get_embedding(query, engine="text-embedding-ada-002")

    df = pd.read_csv('earnings-embeddings.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))

    sorted_by_similarity = df.sort_values("similarities", ascending=False).head(1)
    #print(results)
    results = sorted_by_similarity['text'].values.tolist()

#    results = [item for item in items if query in item]
    # Render the search results template, passing in the search query and results
    #return render_template('search_results.html', query=query, results=results)    
    return results

def get_convo(prompt, engine='text-davinci-003', temp=0.5, top_p=1.0, tokens=60, freq_pen=0.5, pres_pen=0.0, stop=['Customer:']):

    #query = request.args.get('query')
    prompt = prompt.encode(encoding="ASCII", errors='ignore').decode()

    # the prompt isnt getting updated with the new messages
    print(prompt)
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop
        )

    results = response['choices'][0]['text'].strip()
    print("Get_convo results: "+ results)
#    results = [item for item in items if query in item]
    # Render the search results template, passing in the search query and results
    #return render_template('search_results.html', query=query, results=results)    
    return results

"""
if __name__ == '__main__':
    #print("Let's chat! (type 'quit' to exit)")
    conversation = list()
    while True:
        user_input = input('Customer: ')
        conversation.append('Customer: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nELEN:'
        response = get_convo(prompt)
        print('ELEN:', response)
        conversation.append('ELEN: %s' % response)


        #if sentence == "quit":
        #    break

        #resp = get_response(sentence)
        #print(resp)
"""