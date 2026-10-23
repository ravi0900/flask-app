import hashlib
import re
import uuid
from bson import ObjectId
from flask import Flask, jsonify, request
from collections.abc import Mapping
import os
import pymongo
app = Flask(__name__)

# load_dotenv()

from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.getenv('URI'))
db= client.test
collection = db['student_grades_db']
todo_collection = db['todo_items']

@app.route('/')
def home():
    return "Welcome to the Student Grade API!"

@app.route('/api')
def get_student_grades():
    dict_student_grade = {
        "Anjali": 80,
        "Ravi": 80,
        "Ramesh": 70,
        "Suresh": 60,
	    "Harish":90
    }
    return jsonify(dict_student_grade)

@app.route('/view')
def view_student_grades():
    students = list(collection.find({}, {'_id': 0}))
    todo_items = list(todo_collection.find({}, {'_id': 0}))
    return jsonify({
        "students": students,
        "todoItems": todo_items,
    })

@app.route('/submit', methods=['POST'])
def submit_student_grade():
    form_data = request.get_json()
    # print(form_data)
    email = str(form_data.get('email', '')).strip()
    if collection.find_one({'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}}):
        return jsonify({"message": "This email has already been submitted."}), 409
    collection.insert_one(form_data)
    return jsonify({"message": "Data submitted successfully!"})

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json(silent=True) if request.is_json else request.form
    if not isinstance(data, Mapping):
        return jsonify({"error": "A JSON object or form data is required."}), 400

    item_name = data.get('itemName')
    item_description = data.get('itemDescription')
    if not isinstance(item_name, str) or not item_name.strip():
        return jsonify({"error": "itemName is required."}), 400
    if not isinstance(item_description, str) or not item_description.strip():
        return jsonify({"error": "itemDescription is required."}), 400

    item_name = item_name.strip()
    item_description = item_description.strip()
    item_id = ObjectId()
    todo_item = {
        "_id": item_id,
        "itemId": str(item_id),
        "itemName": item_name,
        "itemDescription": item_description,
    }

    todo_collection.insert_one(todo_item)
    return jsonify({"message": "To-do item submitted successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
