from . import blathers_routes
from flask import request, jsonify
from server.utils import *

@blathers_routes.route('/ask', methods=['POST'])
def user_query():
    question = request.json['question']
    answer = None

    if question and len(question) > 0:
        answer = ask(question)

    return jsonify({ "question": question, "answer": answer })    

@blathers_routes.route('/upload', methods=['POST'])
def upload_doc():
    if request.method == 'POST':       
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file:
            handler = validate_file(file)
            if handler:
                filepath = os.path.join(os.getcwd(), "server", "docs", file.filename)

                try:
                    file.save(filepath)
                except Exception as e:
                    print("Save Failed: " + str(e))
                    return jsonify({"error": f"Failed to save file: {e}"}), 500
                
                if handler == "word":
                    results = process_word(file.filename, filepath)

                    if results:
                        return jsonify({"message": "File uploaded successfully."}), 200
                    else:
                        return jsonify({"message": "File uploaded failed."}), 500
            else:
                return jsonify({"error": "Invalid file."}), 400
        else:
            return jsonify({"error": "File not provided."}), 400
    else:
        return jsonify({"error": "Only POST requests are allowed."}), 405
