"""
app.py -    App that connects to a postgres database to create and populate tables representing possible library tables.
            These tables are Users, Addresses, Checkouts, Books, and Reviews.
Jade Harbert
CSC 122
November 13th, 2022
"""
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:michael2001@localhost/app5'

db = SQLAlchemy(app)


class Users(db.Model):
    """
    SQLAlchemy table representing Users with id, full_name, enabled, and last_login columns
    Table shares a 1-1 relationship with addresses and a 1-many relationship with checkouts
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64))
    enabled = db.Column(db.Boolean)
    last_login = db.Column(db.DateTime)

    address = db.relationship('Addresses', back_populates='user', uselist=False)


class Addresses(db.Model):
    """
    SQLAlchemy table representing addresses with user_id, street, city, and state columns
    Table shares a 1-1 relationship with users
    user_id utilizes the id column in users as a foreign key
    """
    __tablename__ = "addresses"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    street = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(2), nullable=False)

    user = db.relationship('Users', back_populates="address")


class Checkouts(db.Model):
    """
    SQLAlchemy table representing checkouts with id, user_id, book_id, checkout_date, and return_date columns
    Table shares a many-to-one relationship with books and users
    user_id and book_id utilize foreign keys from users.id and books.id respectively
    """
    __tablename__ = "checkouts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Foreign Key
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))  # Foreign Key
    checkout_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)

    book = db.relationship("Books", back_populates="checkout")


class Books(db.Model):
    """
    SQLAlchemy table representing books with id, title, author, published_date, and isbn columns
    Table shares a one-to-many relationship with checkouts and reviews
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    isbn = db.Column(db.String(12))

    checkout = db.relationship("Checkouts", back_populates="book")
    review = db.relationship("Reviews", back_populates="book")


class Reviews(db.Model):
    """
    SQLAlchemy table representing reviews with id, book_id, reviewer_name, content, rating, and published_date columns
    Table shares a many-to-one relationship with books
    book_id column utilizes a foreign key from books.id
    """
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    reviewer_name = db.Column(db.String(64))
    content = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    published_date = db.Column(db.DateTime, default=datetime.datetime.now())

    book = db.relationship("Books", back_populates="review")


with app.app_context():
    """
    Creates all the tables in postgres and populates them with data
    """
    db.drop_all()
    db.create_all()

    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    books_list = [Books(id=1, title='My First SQL Book', author='Mary Parker',
                        published_date='2012-02-22 12:08:17.320053-03',
                        isbn='981483029127'),
                  Books(id=2, title='My Second SQL Book', author='John Mayer',
                        published_date='1972-07-03 09:22:45.050088-07',
                        isbn='857300923713'),
                  Books(id=3, title='My Third SQL Book', author='Cary Flint',
                        published_date='2015-10-18 14:05:44.547516-07',
                        isbn='523120967812')]

    reviews_list = [Reviews(id=1, book_id=1, reviewer_name='John Smith',
                            content='My first review', rating=4,
                            published_date='2017-12-10 05:50:11.127281-02'),
                    Reviews(id=2, book_id=2, reviewer_name='John Smith',
                            content='My second review', rating=5,
                            published_date='2017-10-13 15:05:12.673382-05'),
                    Reviews(id=3, book_id=2, reviewer_name='Alice Walker',
                            content='Another review', rating=1,
                            published_date='2017-10-22 23:47:10.407569-07')]

    addresses_list = [Addresses(user_id=1, street='1 Market Street',
                                city='San Francisco', state='CA'),
                      Addresses(user_id=2, street='2 Elm Street',
                                city='San Francisco', state='CA'),
                      Addresses(user_id=3, street='3 Main Street',
                                city='Boston', state='MA')]

    users_list = [Users(id=1, full_name="John Smith", enabled=False,
                        last_login=datetime.datetime.strptime("2017-10-25 10:26:10.015152", datetime_format)),
                  Users(id=2, full_name="Alice Walker", enabled=True,
                        last_login=datetime.datetime.strptime("2017-10-25 10:26:50.295461", datetime_format)),
                  Users(id=3, full_name="Harry Potter", enabled=True,
                        last_login=datetime.datetime.strptime("2017-10-25 10:26:50.295461", datetime_format)),
                  Users(id=5, full_name="Jane Smith", enabled=True,
                        last_login=datetime.datetime.strptime("2017-10-25 10:26:43.324015", datetime_format))]

    checkouts_list = [Checkouts(id=1, user_id=1, book_id=1,
                                checkout_date=datetime.datetime.strptime('2017-10-15 14:43:18.095143',
                                                                         datetime_format),
                                return_date=None),
                      Checkouts(id=2, user_id=1, book_id=2,
                                checkout_date=datetime.datetime.strptime('2017-10-05 16:22:44.593188',
                                                                         datetime_format),
                                return_date=datetime.datetime.strptime('2017-10-13 13:0:12.673382',
                                                                       datetime_format)),
                      Checkouts(id=3, user_id=2, book_id=2,
                                checkout_date=datetime.datetime.strptime('2017-10-15 11:11:24.994973',
                                                                         datetime_format),
                                return_date=datetime.datetime.strptime('2017-10-22 17:47:10.407569',
                                                                       datetime_format)),
                      Checkouts(id=4, user_id=5, book_id=3,
                                checkout_date=datetime.datetime.strptime('2017-10-15 09:27:07.215217',
                                                                         datetime_format),
                                return_date=None)]

    all_lists = reviews_list + books_list + addresses_list + users_list + checkouts_list
    db.session.add_all(all_lists)
    db.session.commit()

if __name__ == '__main__':
    app.run()
