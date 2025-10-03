import pandas
import joblib
import requests
import numpy as np
from    sklearn.metrics.pairwise import cosine_similarity



def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed",json={
        'model':'bge-m3',
        'input':text_list 
    })

    embedding=r.json()['embeddings']
    return embedding


def inference(prompt):
    r = requests.post('http://localhost:11434/api/generate', json={
        'model':'llama3.2',
        'prompt':prompt,
        'stream':False

    })
    response= r.json()
    print(response)
    return response


df = joblib.load('embedding.joblib')

incoming_query = input('ask a question')

embeded_question = create_embedding(incoming_query)[0]

similarity = cosine_similarity(np.vstack(df['embedding']), [embeded_question]).flatten()

top_result= 5
max_idx=similarity.argsort()[::-1][0:top_result]
new_df=df.loc[max_idx]

prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
'''


response=inference(prompt)['response']

print(response)





