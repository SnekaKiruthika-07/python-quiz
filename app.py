from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Sample quiz data
quiz_data = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Rome', 'Berlin'],
        'answer': 'Paris'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {'question': 'What is the square root of 64?', 'options': ['6', '8', '10', '12'], 'answer': '8'},
        {'question': 'Who painted the Mona Lisa?', 'options': ['Van Gogh', 'Picasso', 'Da Vinci', 'Rembrandt'], 'answer': 'Da Vinci'},
        {'question': 'What is the smallest prime number?', 'options': ['1', '2', '3', '5'], 'answer': '2'},
        {'question': 'Which planet is known as the Red Planet?', 'options': ['Earth', 'Mars', 'Jupiter', 'Venus'], 'answer': 'Mars'},
        {'question': 'Which element has the chemical symbol O?', 'options': ['Oxygen', 'Osmium', 'Oganesson', 'Oxide'], 'answer': 'Oxygen'},
        {'question': 'Who wrote "Pride and Prejudice"?', 'options': ['Jane Austen', 'Charles Dickens', 'Mark Twain', 'Emily Bronte'], 'answer': 'Jane Austen'}
]

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('quiz.db')  # Creates a database file named 'quiz.db'
    conn.row_factory = sqlite3.Row  # Makes rows dictionary-like
    return conn

# Function to create the results table if it doesn't exist
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        attempted INTEGER NOT NULL,
                        percentage REAL NOT NULL
                    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        user_answers = {}
        score = 0
        attempted = 0

        for i in range(len(quiz_data)):
            question_key = f'q{i + 1}'
            selected_answer = request.form.get(question_key)
            
            if selected_answer:
                user_answers[question_key] = selected_answer
                attempted += 1
                
                if selected_answer == quiz_data[i]['answer']:
                    score += 1

        total_questions = len(quiz_data)
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Store result in the database
        conn = get_db_connection()
        conn.execute('INSERT INTO quiz_results (name, score, attempted, percentage) VALUES (?, ?, ?, ?)',
                     (name, score, attempted, percentage))
        conn.commit()
        conn.close()

        return render_template('result.html', 
                               name=name, 
                               total_questions=total_questions, 
                               score=score, 
                               percentage=percentage, 
                               attempted=attempted, 
                               user_answers=user_answers, 
                               quiz_data=quiz_data)
    
    return render_template('quiz.html', quiz_data=quiz_data)

@app.route('/results')
def show_results():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM quiz_results').fetchall()
    conn.close()
    return render_template('all_results.html', results=results)

if __name__ == '__main__':
    create_table()  # Ensures table creation at app startup
    app.run(debug=True)
