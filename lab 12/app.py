import faiss
import numpy as np
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

encoder = SentenceTransformer('paraphrase-MiniLM-L3-v2')

documents = [
    "The library is open from 9 AM to 9 PM.",
    "Student IDs can be collected from the registrar office.",
    "The cafeteria serves lunch between 12 PM and 2 PM.",
    "Wifi passwords are provided during orientation."
]

doc_embeddings = encoder.encode(documents)
vector_dim = doc_embeddings.shape[1]
search_index = faiss.IndexFlatL2(vector_dim)
search_index.add(np.array(doc_embeddings).astype('float32'))

@app.route('/')
def main_page():
    return "Vector Search API is running. Use /search endpoint."

@app.route('/search', methods=['POST'])
def semantic_search():
    user_input = request.json.get('prompt')
    query_vector = encoder.encode([user_input])
    

    distance, indices = search_index.search(np.array(query_vector).astype('float32'), 1)
    
    matched_text = documents[indices[0][0]]
    return jsonify({"match": matched_text, "score": float(distance[0][0])})

if __name__ == '__main__':
    app.run(port=9000)