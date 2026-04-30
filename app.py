from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

# 内存存储待办事项
todos = []
todo_id_counter = 0

# 首页路由 - 返回 HTML
@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

# 获取所有待办事项
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# 添加待办事项
@app.route('/todos', methods=['POST'])
def add_todo():
    global todo_id_counter
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'task is required'}), 400
    todo_id_counter += 1
    todo = {
        'id': todo_id_counter,
        'task': data['task'],
        'done': False
    }
    todos.append(todo)
    return jsonify(todo), 201

# 删除待办事项
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'todo not found'}), 404
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({'message': 'deleted'}), 200

# 标记完成/未完成
@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def toggle_todo(todo_id):
    data = request.get_json()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'todo not found'}), 404
    if 'done' not in data:
        return jsonify({'error': 'done field required'}), 400
    todo['done'] = data['done']
    return jsonify(todo), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)