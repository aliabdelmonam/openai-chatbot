from dotenv import load_dotenv
import os
from  openai import AzureOpenAI
from flask import Flask,render_template,request


app = Flask(__name__, template_folder='templates', static_folder='static')

# Load .env from an absolute path
load_dotenv(dotenv_path='aa.env')

client =AzureOpenAI (
    azure_deployment='gpt-35-turbo',
    azure_endpoint=os.getenv('END_POINT'),
    api_key= os.getenv('API_KEY'),
    api_version='2024-12-01-preview'
)

@app.route("/")
def index():
#     response= client.chat.completions.create(
#        messages=[
#             {"role": "user", "content": "What is the capital of India?"}
#         ],
#         model='gpt-35-turbo'
#     )
#     chat_response =response.choices[0].message.content
    return render_template('index.html',chat_response=None)
@app.route('/chat',methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    try:
        response= client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_input}
            ],
            model='gpt-35-turbo'
        )
        chat_response = response.choices[0].message.content
        return render_template('index.html', ai_message=chat_response,user_message = user_input,error_flag=0)
    except Exception as e:
        error_message=str(e)
        return render_template('index.html', error_message=error_message,error_flag=1,user_message=user_input)
if __name__ == '__main__':
    app.run(debug=True)