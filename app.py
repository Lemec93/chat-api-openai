from flask import Flask, render_template, request



import os
from dotenv import load_dotenv
import openai
import json


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

load_dotenv()

def get_Chat_response(text):

    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open('data.json', 'r') as json_file:
        messages = json.load(json_file)

    messages.append({"role": "user", "content": str(text)})

    completion = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:legafrik::7sIthuRQ",
        messages=messages
    )
    chat_completion = completion.choices[0].message.content


    messages.append(completion.choices[0].message)
    messages.append({
        "role": "system",
        "content": "En tant qu'expert en programmation Django."
    })
    with open('data.json', 'w') as json_file:
        json.dump(messages, json_file, indent=4)

    return chat_completion

if __name__ == '__main__':
    app.run()
