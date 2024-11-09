from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Azure OpenAI Settings
openai.api_type = "azure"
openai.api_base = "https://educationhackathon.openai.azure.com/"
openai.api_version = "2024-08-01-preview"
openai.api_key = "API_KEY"

DEPLOYMENT_NAME = "gpt-4o"  # Your GPT-3.5 or GPT-4 deployment name

class AINLPHelper:
    def summarize_text(self, text):
        try:
            prompt = f"Please summarize the following text concisely:\n\n{text}"
            response = openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

    def answer_question(self, context, question):
        try:
            prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
            response = openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

    def generate_questions(self, context):
        try:
            prompt = f"Generate 3 questions based on this text to test understanding:\n\n{context}"
            response = openai.ChatCompletion.create(
                engine=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates relevant and difficult questions based on given text that are made to test understanding."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)

# Initialize NLP Helper
nlp = AINLPHelper()

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = nlp.summarize_text(text)
    return jsonify({'summary': result})

@app.route('/api/answer', methods=['POST'])
def answer():
    data = request.json
    context = data.get('context', '')
    question = data.get('question', '')
    
    if not context or not question:
        return jsonify({'error': 'Context and question are required'}), 400
    
    result = nlp.answer_question(context, question)
    return jsonify({'answer': result})

@app.route('/api/generate-questions', methods=['POST'])
def generate():
    data = request.json
    context = data.get('context', '')
    
    if not context:
        return jsonify({'error': 'Context is required'}), 400
    
    result = nlp.generate_questions(context)
    return jsonify({'questions': result})

if __name__ == '__main__':
    app.run(debug=True)