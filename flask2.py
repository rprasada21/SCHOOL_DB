from flask import Flask
import pymongo
from flask import request
from flask import jsonify
from bson import ObjectId

app = Flask(__name__)

@app.route('/getschools', methods = ['GET'])
def getSchools():
    if request.method == 'GET':
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['SCHOOL']
        collection = db['Schools']
        cursor = collection.find()
        results=[]
        for document in cursor:
            document['_id'] = str(document['_id'])
            results.append(document)
        return jsonify(results)
@app.route('/getteachers', methods = ['GET'])
def getTeachers():
    if request.method == 'GET':
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['SCHOOL']
        collection = db['teachers']
        cursor = collection.find({"school_id":"001"})
        results = []
        for document in cursor:
            document['_id'] = str(document['_id'])
            results.append(document)
        return jsonify(results)
@app.route('/createschool', methods=['POST'])
def add_data():
    data = request.json
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['SCHOOL']
    collection=db['Schools']
    collection.insert_one(data)
    return 'Data added successfully!'

@app.route('/updateschools/<string:school_id>', methods=['PUT'])
def UpdateSchool(school_id):
    if request.method == 'PUT':
        # Get the new data from the request body
        data = request.json

        # Update the document with the specified school_id
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['SCHOOL']
        collection = db['Schools']
        result = collection.update_one(
            {'school_id': school_id},
            {'$set': data}
        )

        # Check if a document was modified
        if result.modified_count > 0:
            # Return a success message
            return 'School updated successfully'
        else:
            # Return a 404 error if no document was found
            return 'School not found', 404


@app.route('/deleteschool/<string:school_id>', methods=['DELETE'])
def DeleteSchool(school_id):
    if request.method == 'DELETE':
        # Connect to the MongoDB server

        # Delete the document with the specified school_id
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['SCHOOL']
        collection = db['Schools']
        result = collection.delete_one({'school_id': school_id})

        # Check if a document was deleted
        if result.deleted_count > 0:
            # Return a success message
            return 'School deleted successfully'
        else:
            # Return a 404 error if no document was found
            return 'School not found', 404






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
