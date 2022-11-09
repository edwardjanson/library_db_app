from flask import Flask, render_template, redirect, request
from flask import Blueprint
import repositories.book_repository as book_repository
import repositories.author_repository as author_repository
from models.author import Author
from models.book import Book


books_blueprint = Blueprint("books", __name__)


@books_blueprint.route("/books")
def books():
    books = book_repository.select_all()
    return render_template("books/index.html", books=books)


@books_blueprint.route("/books/new")
def new_book():
    authors = author_repository.select_all()
    return render_template("books/new.html", all_authors=authors)


@books_blueprint.route("/books", methods=["POST"])
def create_book():
    title = request.form["description"]
    genre = request.form["genre"]
    author_id = request.form["author_id"]

    author = author_repository.select(author_id)
    book = Book(title, genre, author)

    book_repository.save(book)
    return redirect("/books")


@books_blueprint.route("/books/<id>")
def get_book(id):
    book = book_repository.select(id)
    return render_template("/books/details.html", book=book)


@books_blueprint.route("/books/<id>/edit")
def edit_book(id):
    book = book_repository.select(id)
    users = author_repository.select_all()
    return render_template("/books/edit.html", book=book, all_users=users)


@books_blueprint.route("/books/<id>", methods=["POST"])
def update_book(id):
    title = request.form["title"]
    genre = request.form["genre"]
    author_id = request.form["author_id"]
    
    author = author_repository.select(author_id)
    book = Book(title, genre, author, id)

    book_repository.update(book)
    return redirect("/books")

@books_blueprint.route("/books/<id>/delete", methods=["POST"])
def delete_book(id):
    book_repository.delete(id)
    return redirect("/books")