from flask import Flask, render_template, request, jsonify, session
import random
import json
import math

current_step = 0
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Sample math topics and questions database
MATH_DATABASE = {
    "quadratic equations": {
        "questions": [
            {
                "question": "Solve the quadratic equation: x² + 5x + 6 = 0",
                "steps": [
                    {
                        "instruction": "First, let's identify a, b, and c in the equation ax² + bx + c = 0",
                        "sub_question": "What are the values of a, b, and c?",
                        "answer": "a = 1, b = 5, c = 6"
                    },
                    {
                        "instruction": "We can solve this using factorization. The factors of 6 that add up to 5 are...",
                        "sub_question": "What two numbers multiply to give 6 and add to give 5?",
                        "answer": "2 and 3"
                    },
                    {
                        "instruction": "Therefore, we can rewrite the equation as: (x + 2)(x + 3) = 0",
                        "sub_question": "Using the zero product property, what are the values of x?",
                        "answer": "x = -2 or x = -3"
                    }
                ],
                "final_answer": "x = -2 or x = -3"
            }
        ]
    },
    "pythagoras theorem": {
        "questions": [
            {
                "question": "Find the hypotenuse of a right-angled triangle with sides 3cm and 4cm",
                "steps": [
                    {
                        "instruction": "Recall Pythagoras' theorem: a² + b² = c²",
                        "sub_question": "What do we substitute for a and b?",
                        "answer": "a = 3, b = 4"
                    },
                    {
                        "instruction": "Now calculate a² + b²",
                        "sub_question": "What is 3² + 4²?",
                        "answer": "25"
                    },
                    {
                        "instruction": "To find c, take the square root of both sides",
                        "sub_question": "What is √25?",
                        "answer": "5"
                    }
                ],
                "final_answer": "The hypotenuse is 5cm"
            }
        ]
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    topic = request.json.get('topic').lower()
    if topic in MATH_DATABASE:
        return jsonify({"status": "success", "topic": topic})
    return jsonify({"status": "error", "message": "Topic not found"})

@app.route('/get_question', methods=['POST'])
def get_question():
    topic = request.json.get('topic')
    if topic in MATH_DATABASE:
        question = random.choice(MATH_DATABASE[topic]["questions"])
        session['current_question'] = question
        session['current_step'] = 0
        return jsonify({
            "question": question["question"],
            "step": question["steps"][0]["instruction"],
            "sub_question": question["steps"][0]["sub_question"]
        })
    return jsonify({"status": "error", "message": "Topic not found"})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.json.get('answer')
    current_question = session.get('current_question')
    current_step = session.get('current_step')
    
    if not current_question or current_step is None:
        return jsonify({"status": "error", "message": "No active question"})
    
    correct_answer = current_question["steps"][current_step]["answer"]
    is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
    
    response = {
        "is_correct": is_correct,
        "correct_answer": correct_answer
    }
    
    if is_correct:
        current_step += 1
        session['current_step'] = current_step
        
        if current_step < len(current_question["steps"]):
            response["next_step"] = {
                "instruction": current_question["steps"][current_step]["instruction"],
                "sub_question": current_question["steps"][current_step]["sub_question"]
            }
        else:
            response["final_answer"] = current_question["final_answer"]
            
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
