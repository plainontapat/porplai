import pymongo
from flask import Flask,jsonify,render_template,request
from bson import json_util
#from flask_pymongo import PyMongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:DEPxfa35911@10.100.2.119:27017")
#client = pymongo.MongoClient("mongodb://admin:AAGzez02811@node9149-advweb-11.app.ruk-com.cloud:11154")

db = client["PorPlai"]


####### index ###############
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"
    return texts

######### GET ALL #################
@app.route("/user", methods=['GET'])
def get_user():
    char = db.user
    output = char.find()
    
    return json_util.dumps(output)

############## GET ONE ############################
@app.route("/user/<name>", methods=['GET'])
def get_oneuser(name):
    char = db.user
    output = char.find_one({'name' : name})
    
        
    return json_util.dumps(output)

######################### INSERT ####################
@app.route('/user', methods=['POST'])
def add_user():
  char = db.user
  name = request.json['name']
  size = request.json['size']
  price = request.json['price']

  char_id = char.insert({'name': name, 
                        'size': size,
                        'price': price
                       })
  new_char = char.find_one({'_id': char_id })
  output = {'name' : new_char['name'], 'size' : new_char['size'],
                        'price' : new_char['price']
                    
                        }
  return jsonify(output)

# ##################### UPDATE ########################
@app.route('/user/<name>', methods=['PUT'])
def update_user(name):
    char = db.user
    x = char.find_one({'name' : name})
    if x:
        myquery = {'name' : x['name'],'size' : x['size'],
                        'price' : x['price']
                       }

    name = request.json['name']
    size = request.json['size']
    price = request.json['price']
 
    
    newvalues = {"$set" : {'name' : name, 'size' : size,
                        'price' : price,
                        }}

    char_id = char.update_one(myquery, newvalues)

    output = {'name' : name, 'size' : size,
                        'price' : price,
                        }

    return jsonify(output)

##################### DELETE ############################ 
@app.route('/user/<name>', methods=['DELETE'])
def delete_user(name):
    char = db.user
    x = char.find_one({'name' : name})

    char_id = char.delete_one(x)

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)