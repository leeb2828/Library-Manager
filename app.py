from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import routes
import os 


def create_the_database(db):
    db.create_all() # create_all() comes with flask sqlalchemy

app = Flask(__name__)
app.config['SECRET KEY'] = 'A secret'

all_methods = ['GET', 'POST']
# Home page (that shows all the books)
app.add_url_rule('/', methods=all_methods, view_func=routes.home_route)
app.add_url_rule('/addnewbook', view_func=routes.new_book)
app.add_url_rule('/viewbook<title>/<author>/<genre>/<year>', view_func=routes.view_book)
app.add_url_rule('/editbook<title>/<author>/<genre>/<year>', methods=all_methods, view_func=routes.edit_book)
app.add_url_rule('/deletebook<title>/<author>', methods=all_methods, view_func=routes.delete_book)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # no warning messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

# Create the Book Table
class Books(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)


# Insert new book into library database
def insert_new_book(title, author, genre, year):
    new_book = Books(title=title, author=author, genre=genre, year=year)
    db.session.add(new_book)
    db.session.commit()


# Modify Book Information
# Takes in dictionary, title, author
def modify_book_info(items_to_modify, the_title, the_author):
    the_book = Books.query.filter_by(title=the_title, author=the_author).first()

    if items_to_modify['title']:
        the_book.title = items_to_modify['title']
    if items_to_modify['author']:
        the_book.author = items_to_modify['author']
    if items_to_modify['genre']:
        the_book.genre = items_to_modify['genre']
    if items_to_modify['year']:
        the_book.year = items_to_modify['year']
    
    db.session.commit()


# Delete book from the library
def delete_book(the_title, the_author):
    book_to_delete = Books.query.filter_by(title=the_title, author=the_author).first()
    db.session.delete(book_to_delete)
    db.session.commit()


# check if entry already exists
def check_entry(title, author):
    check_book = Books.query.filter_by(title=title, author=author).first()
    if (check_book):
        return True 
    else: 
        return False 


# Get all the books from library
def get_all_books():
    all_books_in_library = Books.query.all()
    return all_books_in_library


# if database does not exist, create it!
db_is_new = not os.path.exists('library.db')
if db_is_new:
    create_the_database(db)


if __name__ == '__main__':
    app.run(debug=True)
    