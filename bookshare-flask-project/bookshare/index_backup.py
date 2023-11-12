from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()

# change string to the name of your database; add path if necessary
db_name = 'bookshare.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection - and nothing more
@app.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>Connects Successfully</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String)
    Genre = db.Column(db.String)
    Author = db.Column(db.String)
    Condition = db.Column(db.String)

    def __init__(self, Title, Genre, Author, Condition):
        self.Title = Title
        self.Genre = Genre
        self.Author = Author
        self.Condition = Condition

books = [
    { 'Title': 'Gone with the wind', 'Genre': 'Fiction', 'Author': 'Margaret Mitchell', 'Condition':'Good' }
]

@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    Title = "Gone with the wind"
    Genre = "Fiction"
    Author = "MMitchell"
    Condition = "True"
    record = Book(Title, Genre, Author, Condition)
    # Flask-SQLAlchemy magic adds record to database
    db.session.add(record)
    db.session.commit()
    return '', 204

@app.route('/books')
def get_books():
    return jsonify(books)


@app.route('/books', methods=['POST'])
def add_book():
    books.append(request.get_json())
    return '', 204