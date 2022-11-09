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
    return render_template("books/new.html", all_authors=authors, error=False)


@books_blueprint.route("/books", methods=["POST"])
def create_book():
    authors = author_repository.select_all()

    book_title = request.form["title"]
    book_author = request.form["author"]
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






@app.route("/books/search", methods=["GET"])
def search_book():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")

    # Return a list of books that matches the search
    updated_books_list = library.book_list.copy()
    for book in library.book_list:
        if title and title not in book.title:
            updated_books_list.remove(book)
            continue
        if author and author not in book.author:
            updated_books_list.remove(book)
            continue
        if genre and genre not in book.genre:
            updated_books_list.remove(book)
            continue

    return render_template("books.html", books=updated_books_list, error=False)

@app.route('/books/<hyphenated_title>/delete', methods=['POST'])
def delete_book(hyphenated_title):
    book = library.get_book(hyphenated_title)
    library.remove_book(book)
    return redirect("/books")

@app.route('/books/<hyphenated_title>/update', methods=['POST'])
def update_book_check_out_status(hyphenated_title):
    # Update the check-out status based on user selection
    book = library.get_book(hyphenated_title)
    status = request.form.getlist("check-out-status")
    library.update_check_out_status(book, status)

    # Load page where the form submission occurred
    location = request.args.get("loc")
    if location == "book":
        return render_template("book.html", book=book)
    else:
        return redirect("/books")