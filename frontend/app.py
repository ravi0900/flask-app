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
    try:
        response = requests.post('http://localhost:9000/submit', json=form_data, timeout=5)
    except requests.RequestException:
        return render_template(
            'index.html',
            current_time=datetime.datetime.now(),
            form_data=form_data,
            error='Could not submit your information right now. Please try again.',
        ), 502

    if response.status_code == 409:
        return render_template(
            'index.html',
            current_time=datetime.datetime.now(),
            form_data=form_data,
            error='This email has already been submitted.',
        ), 409

    response.raise_for_status()
    return "Data submitted successfully"


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