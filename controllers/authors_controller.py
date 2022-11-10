from flask import Flask, render_template, redirect, request
from flask import Blueprint
import repositories.book_repository as book_repository
import repositories.author_repository as author_repository
from models.author import Author
from models.book import Book


authors_blueprint = Blueprint("authors", __name__)


# @authors_blueprint.route("/authors")
# def authors():
#     authors = author_repository.select_all()
#     return render_template("index.html", all_authors=authors)


@authors_blueprint.route("/authors/new")
def new_author():
    return render_template("authors/new.html", error=False)


@authors_blueprint.route("/authors/new", methods=["POST"])
def create_author():
    authors = author_repository.select_all()

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    # Show error message if a form field is missing
    if first_name == "" or last_name == "":
        return render_template("authors/new.html", error=True) 

    author = Author(first_name, last_name)

    author_repository.save(author)
    return redirect("/books")


# @authors_blueprint.route("/authors/<id>")
# def get_author(id):
#     author = author_repository.select(id)
#     return render_template("authors/index.html", author=author)


# @authors_blueprint.route("/authors/<id>/edit")
# def edit_author(id):
#     author = author_repository.select(id)
#     authors = author_repository.select_all()
#     return render_template("authors/edit.html", author=author, all_authors=authors)


# @authors_blueprint.route("/authors/<id>", methods=["POST"])
# def update_author(id):
#     title = request.form["title"]
#     genre = request.form["genre"]
#     author_id = request.form["author_id"]
    
#     author = author_repository.select(author_id)
#     author = author(title, genre, author, id)

#     author_repository.update(author)
#     return redirect("/authors")


# @authors_blueprint.route("/authors/<id>/delete", methods=["POST"])
# def delete_author(id):
#     author_repository.delete(id)
#     return redirect("/authors")