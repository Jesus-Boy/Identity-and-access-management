import os
from turtle import title
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    all_drinks = Drink.query.all()
    try:
      drinks = [drink.short() for drink in all_drinks]
      return jsonify({
        'success': True,
        'drinks': drinks
      }, 200)
    except:
      abort(422)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_details(payload):
    all_drinks = Drink.query.all()
    try:
      drinks = [drinks.long() for drinks in all_drinks]
      return jsonify({
        "success": True, 
        "drinks": drinks
      }, 200)
    except:
      abort(404)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    body = request.json
    title = body['title']
    recipe = body['recipe']
    try:
      # creating and inserting the new drink to the database
      new_drink = Drink(title= title, recipe= json.dumps(recipe))
      new_drink.insert()
      return jsonify({
        'success': True,
        'drinks': new_drink
      }, 200)
    except:
      abort(400)
    

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods= ['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
  body = request.json
  updated_title = body['title']
  updated_recipe = body['recipe']
  drink = Drink.query.get(id)
  try:
    drink = Drink(title= updated_title, recipe= json.dumps(updated_recipe))
    drink.update()
    return jsonify({
      "success": True, 
      "drinks": drink.long()
    })
  except:
    abort(404)



  
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.get(id)
    try:
      drink.delete()
      return jsonify({
        'success': True,
        'deleted': id
      }, 200)
    except:
      abort(422)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
  return jsonify({
    'success': False,
    'error': 400,
    'message': 'bad request.'
  }), 400

@app.errorhandler(401)
def unauthorized(error):
  return jsonify({
    'success': False,
    'error': 401,
    'message': 'unauthorized.'
  }), 401
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message': 'resource not found.'
  }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error_handler(exp):

  return jsonify({
    'success': False,
    'error': exp.status_code,
    'message': exp.error
  })