from flask import Flask, jsonify, request
import os
import pymongo
app = Flask(__name__)

# load_dotenv()

from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.getenv('URI'))
db= client.test
collection = db['student_grades_db']

@app.route('/')
def home():
    return "Welcome to the Student Grade API!"

@app.route('/api')
def get_student_grades():
    dict_stuent_grade = {
        "Anjali": 90,
        "Ravi": 80,
        "Ramesh": 70,
        "Suresh": 60,
	"Harish":90
    }
    return jsonify(dict_stuent_grade)

@app.route('/view')
def view_student_grades():
    data = collection.find()
    data = list(data)
    for item in data:
        print(item)
        del item['_id']  # Remove the '_id' field from each document
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def submit_student_grade():
    form_data = request.get_json()
    # print(form_data)
    collection.insert_one(form_data)
    return jsonify({"message": "Data submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
