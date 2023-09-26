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

# Check if logo lmn.jpg already exists in MongoDB
if db.linktree.find_one({'logo': 'logo lmn.jpg'}) is None:
    # Logo does not exist in MongoDB, save it
    with open('static/logo lmn.jpg', 'rb') as f:
        image_data = f.read()

    db.linktree.insert_one({'logo': 'logo lmn.jpg', 'image_data': image_data})

app = Flask(__name__)

# Cache logo data in memory
logo_data = None

@app.route('/')
def home():

    global logo_data
    if logo_data is None:
        # Get logo from MongoDB
        logo_data = db.linktree.find_one({'logo': 'logo lmn.jpg'})['image_data']

    # Return rendered template with logo data
    return render_template('index.html', logo_data=logo_data)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
