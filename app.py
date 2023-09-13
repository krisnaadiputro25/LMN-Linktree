import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Check if collection already exists
if 'linktree' in db.list_collection_names():
    # Collection already exists, do nothing
    print('Collection linktree already exists')
else:
    # Collection does not exist, create it
    db.create_collection('linktree')

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

# Add code to save the logo file to MongoDB

# Get the collection
collection = db['linktree']

# Insert the logo file into the collection
logo_file = open('static/logo lmn.jpg', 'rb')
logo_data = logo_file.read()

document = {
    'logo': logo_data
}

collection.insert_one(document)

# Add code to save the Linktree images to MongoDB


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
