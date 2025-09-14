# person.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

notes = []

@app.route('/api/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    note = data.get('note')
    if note:
        notes.append(note)
        return jsonify({'status': 'success', 'message': 'Note saved!'})
    return jsonify({'status': 'error', 'message': 'Empty note'}), 400

@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'answer': 'Please ask a valid question.'}), 400

    matching_notes = [n for n in notes if query.lower() in n.lower()]
    answer = matching_notes[0] if matching_notes else "No relevant notes found."
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
