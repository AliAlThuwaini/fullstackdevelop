
from operator import truediv
import random
import os
from flask import Flask, request, abort, jsonify
from flask.globals import current_app


from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
from models import setup_db, Book





BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there. 
#     If you do not update the endpoints, the lab will not work - of no fault of your API code! 
#   - Make sure for each route that you're thinking through when to abort and with which kind of error 
#   - If you change any of the response body keys, make sure you update the frontend to correspond. 



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



  
  #Error handler decorator. It has to contain the following:
  #error code as argument in the decorator, message, returned error code at the end
  #Multiple errorhandler decorator can be defined with different error codes to handle different error types and return json response instead of html code!

  @app.errorhandler(404)
  def not_found(error): #the argument 'error' is not mandatory here as we're not using it!
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not found"
        }), 404

  @app.errorhandler(422)
  def not_processable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Resource is unprocessable"
        }), 422

  @app.errorhandler(400)
  def not_processable(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

  @app.errorhandler(405)
  def not_processable(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "method not allowed"
        }), 405


  @app.route('/')
  def root_message():
    return jsonify({
      'message': "Welcome, you're in the root page"
    })



  # @TODO: Write a route that retrivies all books, paginated. 
  #         You can use the constant above to paginate by eight books.
  #         If you decide to change the number of books per page,
  #         update the frontend to handle additional books in the styling and pagination
  #         Response body keys: 'success', 'books' and 'total_books'
  # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

  #Ali: This is my work and the function works perfectly as intended
  # @app.route('/books')
  # def get_books():

  #   book_shelf = request.args.get('page', 1, type=int)
  #   start_index = (book_shelf - 1) * BOOKS_PER_SHELF
  #   end_index = start_index + BOOKS_PER_SHELF

  #   books = Book.query.all()
  #   #print('type: ', type(books), '/n/n/n')
  #   formatted_books = [book.format() for book in books]
  #   #print('type2: ', type(books), '/n/n/n')
  #   return jsonify({
  #     'success': True,
  #     'books': formatted_books[start_index : end_index],
  #     'total_books': len(formatted_books)
  #   })

  # The below is a more ogrganized code taken from the vedios. Although the above works, the below is a better code I think:

  #Define a helper method:
  def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)  
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books


  @app.route('/books')
  def retrieve_books():
    selection = Book.query.order_by(Book.id).all()
    current_books = paginate_books(request, selection)

    #handle errors in case no returned books
    if len(current_books) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'books': current_books,
      'total_books': len(selection)
    })


  

  # @TODO: Write a route that will update a single book's rating. 
  #         It should only be able to update the rating, not the entire representation
  #         and should follow API design principles regarding method and route.  
  #         Response body keys: 'success'
  # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def update_book(book_id):
    body = request.get_json()
    print ('Before the try block')

    try:
      book = Book.query.filter(Book.id==book_id).one_or_none()
      if book is None:
        abort(404)
      print ('in the Try block')

      if 'rating' in body:
        book.rating = int(body.get('rating'))

      book.update()

      return ({
        'success': True,
        'id': book.id
      })

    except:
      print ('tin the except block')
      abort(400)



  # @TODO: Write a route that will delete a single book. 
  #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
  #        Response body keys: 'success', 'books' and 'total_books'

  @app.route('/books/<int:book_id>', methods=['DELETE'])
  def delete_book(book_id):

    try:
      book = Book.query.filter(Book.id==book_id).one_or_none()

      if book is None:
        abort(404)

      book.delete()
      selection = Book.query.order_by(Book.id).all()
      current_books = paginate_books(request, selection)

      return jsonify({
        'success': True,
        'deleted': book_id,
        'books': current_books,
        'total_books': len(selection)
      })

    except:
      abort(422)




  # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.


  # @TODO: Write a route that create a new book. 
  #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
  # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books. 
  #       Your new book should show up immediately after you submit it at the end of the page. 

  @app.route('/books', methods= ['POST'])
  def create_book():
    body= request.get_json()

    new_title = body.get('title', None)
    new_author = body.get('author', None)
    new_rating = body.get('rating', None)

    try:
      book = Book(title=new_title, author=new_author, rating=new_rating)
      book.insert()

      selection = Book.query.order_by(Book.id).all()
      current_books = paginate_books(request, selection)

      return jsonify({
        'success': True,
        'created': book.id,
        'books': current_books,
        'total_books': len(selection)
      })

    except:
      abort(422)


  
  return app

    