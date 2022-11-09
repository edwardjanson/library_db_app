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
    return render_template("index.html", books=books)


@books_blueprint.route("/books/new")
def new_book():
    authors = author_repository.select_all()
    return render_template("books/new.html", all_authors=authors, error=False)


@books_blueprint.route("/books/new", methods=["POST"])
def create_book():
    authors = author_repository.select_all()

    book_title = request.form["title"]
    book_author = request.form["author_id"]
    book_genre = request.form["genre"]

    # Show error message if a form field is missing
    if book_title == "" or book_author == "" or book_genre == "":
        return render_template("books/new.html", all_authors=authors, error=True) 

    author = author_repository.select(book_author)
    book = Book(book_title, book_genre, author)

    book_repository.save(book)
    return redirect("/books")


@books_blueprint.route("/books/<id>")
def get_book(id):
    book = book_repository.select(id)
    return render_template("books/index.html", book=book)


@books_blueprint.route("/books/<id>/edit")
def edit_book(id):
    book = book_repository.select(id)
    authors = author_repository.select_all()
    return render_template("books/edit.html", book=book, all_authors=authors)


@books_blueprint.route('/books/<id>/change-status', methods=['POST'])
def update_book_check_out_status(id):
    # Update the check-out status based on user selection
    book = book_repository.select(id)
    status = request.form.getlist("check-out-status")
    book.update_check_out(status)
    book_repository.update(book)

    # Load page where the form submission occurred
    location = request.args.get("loc")
    if location == "book":
        return render_template("books/index.html", book=book)
    else:
        return redirect("/books")


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


@books_blueprint.route("/books")
def search_book():
    book_title = request.args.get("title")
    book_author = request.args.get("author")
    book_genre = request.args.get("genre")

    # Return a list of books that matches the search
    book_list = book_repository.select_all()
    books_found = book_list
    for book in book_list:
        if book_title and book_title not in book.title:
            books_found.remove(book)
            continue
        if book_author and book_author not in book.author.first_name or book_author not in book.author.last_name:
            books_found.remove(book)
            continue
        if book_genre and book_genre not in book.genre:
            books_found.remove(book)
            continue

    return render_template("index.html", books=books_found, error=False)