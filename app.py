# Imports Used
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from datetime import datetime

# Creating an instance of a flask appliation
app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/school'
# Initialize MongoDB connection (connect app to MongoDB)
mongo = PyMongo(app)

# changing route to add a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    _json = request.json  # store and convert coming json information from the request

    _studentId = _json["student_id"]
    _fName = _json["first_name"]
    _lName = _json["last_name"]
    _age = _json["age"]
    _gender = _json["gender"]
    _imageURL = _json["image"]
    _active = _json["active"]
    _isDeleted = _json["is_deleted"]

    # Parse the date string from the request and convert it into a Python datetime object
    date_format = "%Y-%m-%d"
    _created = datetime.strptime(_json["created"], date_format)
    _lastUpdated = datetime.strptime(_json["last_updated"], date_format)

    _createdBy = _json["created_by"]
    _lastUpdatedBy = _json["last_updated_by"]

    # Validation (Check if method is POST)
    if request.method == 'POST':
        
        # Inserting the variables into the "students" database
        id = mongo.db.students.insert_one(
            {'student_id': _studentId, 
             'first_name': _fName, 
             'last_name': _lName,
             'age': _age,
             'gender': _gender,
             'image': _imageURL,
             'active': _active,
             'is_deleted': _isDeleted,
             'created': _created,
             'created_by': _createdBy,
             'last_updated': _lastUpdated,
             'last_updated_by': _lastUpdatedBy
             }
            )
        # Generate a response
        response = jsonify("Student added successfully!")

        # Return the response and status code
        return response, 200

    else:
        return not_found()
    

# Changing route to a POST (add) request to add multiple students
@app.route('/add_students', methods=['POST'])
def add_students():
    students_list = request.json  # Store and convert incoming JSON from the request

    if students_list:
        # Loop over each student in the list
        for student_data in students_list:
            _studentId = student_data.get("student_id")
            _fName = student_data.get("first_name")
            _lName = student_data.get("last_name")
            _age = student_data.get("age")
            _gender = student_data.get("gender")
            _imageURL = student_data.get("image")
            _active = student_data.get("active")
            _isDeleted = student_data.get("is_deleted")
            _created = datetime.strptime(student_data.get("created"), "%Y-%m-%d")
            _createdBy = student_data.get("created_by")
            _lastUpdated = datetime.strptime(student_data.get("last_updated"), "%Y-%m-%d")
            _lastUpdatedBy = student_data.get("last_updated_by")

            # Insert the variables into the "students" database
            result = mongo.db.students.insert_one(
                {
                    'student_id': _studentId,
                    'first_name': _fName,
                    'last_name': _lName,
                    'age': _age,
                    'gender': _gender,
                    'image': _imageURL,
                    'active': _active,
                    'is_deleted': _isDeleted,
                    'created': _created,
                    'created_by': _createdBy,
                    'last_updated': _lastUpdated,
                    'last_updated_by': _lastUpdatedBy
                }
            )

        # Generate a response
        response = 'Students added successfully'
        return jsonify(response), 200
    else:
        return not_found()


# Get a student by student_id
@app.route('/get_student/<student_id>', methods=['GET'])
def get_single_student(student_id):
    student = mongo.db.students.find_one({'student_id': student_id})
    if student:
        # Convert the ObjectId to a string
        student['_id'] = str(student['_id'])
        return jsonify(student)
    else:
        return not_found()
    
# Get all students
@app.route('/get_students', methods=['GET'])
def get_all_students():
    students = list(mongo.db.students.find())

    if students:
        # Convert ObjectId to string for each student
        for student in students:
            student['_id'] = str(student['_id'])

        return jsonify(students), 200
    else:
        return not_found()

# Update a student by student_id
@app.route('/update_student/<student_id>', methods=['PUT'])
def update_student(student_id):
    _json = request.json
    date_format = "%Y-%m-%d"
    
    updated_student = {
        'student_id': _json["student_id"],
        'first_name': _json["first_name"],
        'last_name': _json["last_name"],
        'age': _json["age"],
        'gender': _json["gender"],
        'image': _json["image"],
        'active': _json["active"],
        'created': datetime.strptime(_json["created"], date_format),
        'created_by': _json["created_by"],
        'last_updated': datetime.strptime(_json["last_updated"], date_format),
        'last_updated_by': _json["last_updated_by"]
    }
    result = mongo.db.students.update_one(
        {'student_id': student_id},
        {'$set': updated_student}
    )
    if result.modified_count:
        return jsonify('Student updated successfully'), 200
    else:
        return not_found()

# Soft delete a student by student_id
@app.route('/soft_delete_student/<student_id>', methods=['DELETE'])
def soft_delete_student(student_id):
    result = mongo.db.students.update_one(
        {'student_id': student_id},
        # Setting the is_deleted flag to True
        {'$set': {'is_deleted': True}}
    )
    if result.modified_count:
        return jsonify('Student soft deleted successfully'), 200
    else:
        return not_found()
    
# Hard delete a student by student_id
@app.route('/hard_delete_student/<student_id>', methods=['DELETE'])
def hard_delete_student(student_id):
    result = mongo.db.students.delete_one({'student_id': student_id})
    if result.deleted_count:
        return jsonify('Student hard deleted successfully'), 200
    else:
        return not_found()
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ API Methods for the 2nd collection "student_tasks" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get a students' task (using task ID)
@app.route('/get_student_task/<task_id>', methods=['GET'])
def get_student_task(task_id):
    task = mongo.db.student_tasks.find_one({'task_id': task_id})
    if task:
        # Convert the ObjectId to a string
        task['_id'] = str(task['_id'])
        return jsonify(task), 200
    else:
        return not_found()
    
# Get a students' tasks (using student ID)
@app.route('/get_student_tasks/<student_id>', methods=['GET'])
def get_student_tasks(student_id):
    tasks = list(mongo.db.student_tasks.find({'student_id': student_id}))

    if tasks != None:
        # Convert ObjectId to string for each task
        for task in tasks:
            task['_id'] = str(task['_id'])

        return jsonify(tasks), 200
    else:
        return not_found()
    
# Inserting a new task (Single task) for a student
@app.route('/add_student_task', methods=['POST'])
def add_student_task():
    # Storing all the supplied JSON from the request
    _json = request.json
    date_format = "%Y-%m-%d"
    #
    _task_id = _json.get("task_id")
    _student_id = _json.get("student_id")
    _score = _json.get("score")
    _is_deleted = _json.get("is_deleted")
    _created = _json.get("created")
    _created_by = _json.get("created_by")
    last_updated = _json.get("last_updated")
    last_updated_by = _json.get("last_updated_by")

    if request.method == 'POST':
        result = mongo.db.student_tasks.insert_one(
            {
                'task_id': _task_id,
                'student_id': _student_id,
                'score': _score,
                'is_deleted': _is_deleted,
                'created': datetime.strptime(_created, date_format),
                'created_by': _created_by,
                'last_updated': datetime.strptime(last_updated, date_format),
                'last_updated_by': last_updated_by
            }
        )
        return jsonify('Task added successfully'), 200
    else:
        return not_found()
    
# Updating a single student task (Using Task ID):
@app.route('/update_student_task/<task_id>', methods=['PUT'])
def update_student_task(task_id):
    #collect information from the request 
    _json = request.json
    date_format = "%Y-%m-%d"

    updated_student_task = {
        'task_id': _json["task_id"],
        'student_id': _json["student_id"],
        'score': _json["score"],
        'is_deleted': _json["is_deleted"],
        'created': datetime.strptime(_json["created"], date_format),
        'created_by': _json["created_by"],
        'last_updated': datetime.strptime(_json["last_updated"], date_format),
        'last_updated_by': _json["last_updated_by"]
    }
    result = mongo.db.student_tasks.update_one(
        {'task_id': task_id},
        {'$set': updated_student_task}
    )

    if result.modified_count:
        return jsonify('Task updated successfully'), 200
    else:
        return not_found()
    
# Soft Deleting a single task for a student (using task id)
@app.route('/soft_delete_student_task/<task_id>', methods=['DELETE'])
def soft_delete_student_task(task_id):
    result = mongo.db.student_tasks.update_one(
        {'task_id': task_id},
        {'$set': {'is_deleted': True}}
    )
    if result.modified_count:
        return jsonify('Task soft deleted successfully'), 200
    else:
        return not_found()

# Hard Deleting a single task for a student (using task id)
@app.route('/hard_delete_student_task/<task_id>', methods=['DELETE'])
def hard_delete_student_task(task_id):
    result = mongo.db.student_tasks.delete_one({'task_id': task_id})
    if result.deleted_count:
        return jsonify('Task hard deleted successfully'), 200
    else:
        return not_found()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ For Error Handling ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    response = jsonify(message)
    return response, 404

if __name__ == '__main__':
    app.run(debug=True)