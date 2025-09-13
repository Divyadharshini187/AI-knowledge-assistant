from flask import Flask, request, jsonify
from flask_cors import CORS # For handling cross-origin requests
import sqlite3
import os
from transformers import pipeline # For a basic QA model later
# from sentence_transformers import SentenceTransformer # For embeddings

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

DATABASE = 'knowledge_base.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, -- 'note', 'document', 'web_clip'
            title TEXT NOT NULL,
            original_content TEXT, -- Original HTML/Markdown for notes, URL for web, filename for doc
            extracted_text TEXT NOT NULL, -- All content as plain text for search/AI
            tags TEXT, -- Comma-separated tags
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            -- embedding BLOB -- For storing numpy arrays as blobs
        );
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
with app.app_context():
    init_db()

# Dummy Embedding Model (replace with actual sentence-transformers)
# model = SentenceTransformer('all-MiniLM-L6-v2')
# def get_embedding(text):
#     return model.encode(text).tobytes() # Store as bytes

# --- API Endpoints ---

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags', '')

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO content (type, title, original_content, extracted_text, tags) VALUES (?, ?, ?, ?, ?)",
        ('note', title, content, content, tags) # For notes, original and extracted are same
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Note added successfully!"}), 201

@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM content WHERE type = 'note' ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(note) for note in notes])

@app.route('/api/search', methods=['GET'])
def search_content():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    conn = get_db_connection()
    # Simple LIKE search - replace with FTS for better performance
    results = conn.execute(
        "SELECT * FROM content WHERE title LIKE ? OR extracted_text LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
        (f'%{query}%', f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()
    return jsonify([dict(item) for item in results])

# --- Basic AI Query (using pipeline for demonstration) ---
# For a real LLM, you'd feed relevant 'extracted_text' as context.
# Here, it just answers based on query.

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # In a real scenario, you'd perform semantic search here
    # to find relevant documents from your 'extracted_text' column,
    # then pass those documents as 'context' to the LLM.

    # For this demo, let's just make up some context or use a general QA.
    # Imagine 'relevant_docs' is a list of text strings found via semantic search.
    # For now, we'll give it a general context.
    general_context = "The marketing meeting discussed new product features, budget allocations, and a Q3 campaign launch. Key decisions included prioritizing mobile app development and increasing social media ad spend."

    # This pipeline expects a question and a context.
    try:
        answer = qa_pipeline(question=user_question, context=general_context)
        return jsonify({"answer": answer['answer']})
    except Exception as e:
        print(f"Error during AI query: {e}")
        return jsonify({"error": "Failed to process AI query"}), 500


if __name__ == '__main__':
    app.run(debug=True) # debug=True for development