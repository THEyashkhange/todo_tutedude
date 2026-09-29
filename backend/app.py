import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database(os.getenv('DB_NAME'))
connect = db[os.getenv('COLLECTION_NAME')]

backend_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(backend_dir, '..', 'frontend', 'templates')
app = Flask(__name__, template_folder=frontend_dir)

@app.route('/')
def show_todo():
    todos = list(connect.find({}, {"_id": 0}))
    return render_template('index.html', todos=todos)

@app.route('/submittodoitem', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')
        
        if item_name:
            add_list = {
                "itemName": item_name,
                "itemDescription": item_description
            }
            connect.insert_one(add_list)
            return redirect(url_for('show_todo'))
            
    return render_template('add_todo.html')

if __name__ == "__main__":
    app.run(debug=True)
