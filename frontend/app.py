from flask import Flask, jsonify, request, render_template
import os
import datetime 
import requests

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.datetime.now()
    return render_template('index.html', current_time=current_time)

@app.route('/submit' , methods=['POST'])
def submit_student_grade():
    form_data = dict(request.form)
    
    requests.post('http://localhost:9000/submit', json=form_data)
    # Process the submitted data (e.g., save to database)
    return "Data submitted successfully!" 
    # return name

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    form_data = dict(request.form)
    response = requests.post(
        'http://localhost:9000/submittodoitem',
        json=form_data,
    )
    return "Todo item submitted successfully!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)