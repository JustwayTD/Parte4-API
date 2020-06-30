from flask import Flask 
from flask import request
from flask import render_template , url_for, make_response
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
from flask import jsonify,abort

client = MongoClient("mongodb+srv://josel12:passsword@cluster0-rytv6.mongodb.net/Slangs?retryWrites=true&w=majority")
db = client["Slangs"]
collection = db["slangs"]

app = Flask(__name__)

tasks = []
lib = db.slangs.find({},{"_id" :1,"word":1,"meaning":1})
for x in lib:
    tasks.append(x)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['_id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'word' in request.json:
        abort(400)
    task = {
        '_id': tasks[-1]['_id'] + 1,
        'word': request.json['word'],
        'meaning': request.json.get('meaning', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['_id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'word' in request.json and type(request.json['word']) != unicode:
        abort(400)
    if 'meaning' in request.json and type(request.json['meaning']) is not unicode:
        abort(400)
)
    task[0]['word'] = request.json.get('word', task[0]['word'])
    task[0]['meaning'] = request.json.get('meaning', task[0]['meaning'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['_id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
if __name__ == '__main__':
    app.run(debug=True)