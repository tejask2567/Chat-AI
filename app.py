from flask import Flask, request, render_template, session,jsonify
from flask_session import Session
import prompt
import os
from werkzeug.utils import secure_filename
from ingest import ingest
from llmware import llmware
from llmlite import get_completion
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './uploads'
Session(app)

bool1=False
count=0
def handle_document_upload(file,prompt):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    session['document_uploaded'] = f"Document {filename} uploaded."
    ingest()
    response=llmware(prompt)
    return response

def handle_text_input(user_prompt):
    enabled_scanners, settings = prompt.init_settings()
    vault = prompt.Vault()
    sanitized_prompt, results = prompt.scan(vault, enabled_scanners, settings, user_prompt)
    try:
        mappings = prompt.map_redactions(user_prompt, sanitized_prompt)
    except IndexError:
        mappings={}
    session['mappings'] = mappings
    return sanitized_prompt

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    user_input = request.form['message']
    model=request.form['ai_model']
    file = request.files.get('file')
    print(model)
    sanitized_prompt=handle_text_input(user_input)
    if file and request.files['file'].filename != '':
        ai_response=handle_document_upload(file=file,prompt=sanitized_prompt)
    elif model!="" :
        if model=='gpt-3.5-turbo':
            ai_response=get_completion(user_input,model='gpt-3.5-turbo')
        elif model=='gemini/gemini-pro':
            ai_response=get_completion(user_input,model='gemini/gemini-pro')
    mappings = session.get('mappings', {})
    replaced_prompt = prompt.replace_redactions_with_originals(ai_response, mappings)
    return jsonify({"response": replaced_prompt})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)