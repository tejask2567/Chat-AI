from dotenv import load_dotenv
from flask import Flask, render_template, request
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatLiteLLM
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("openai_api_key") 
# os.environ["HUGGINGFACE_API_KEY"] = os.getenv("huggingface_api_key")  
os.environ['GEMINI_API_KEY']= os.getenv('gemini_api_key')  

app = Flask(__name__)

memory=ConversationBufferMemory()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        model = request.form['model']
        response = get_completion(text, model)
        return render_template('index.html', text=text, model=model, response=response)
    return render_template('index.html')

def get_completion(text, model):
    llm = ChatLiteLLM(model=model,client= 'Any')
    conversation = ConversationChain(
        llm=llm, verbose=True, memory=memory
    )
    return conversation.predict(input=text)

if __name__ == '__main__':
    app.run(debug=True)
