from db.run_sql import run_sql
import pdb

from models.book import Book
import repositories.author_repository as author_repository


def save(book):
    sql = "INSERT INTO books (title, genre, author_id, is_checked_out, check_out_logs) VALUES (%s, %s, %s, %s, %s) RETURNING *"
    values = [book.title, book.genre, book.author.id, book.is_checked_out, book.check_out_logs]
    results = run_sql(sql, values)
    id = results[0]['id']
    book.id = id
    return book


def select_all():
    books = []

    sql = "SELECT * FROM books"
    results = run_sql(sql)

    for row in results:
        author = author_repository.select(row['author_id'])
        book = Book(row['title'], row['genre'], author, row['id'], row['is_checked_out'], row['check_out_logs'])
        books.append(book)
    return books


def select(id):
    book = None
    sql = "SELECT * FROM books WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        author = author_repository.select(result['author_id'])
        book = Book(result['title'], result['genre'], author, result['id'], result['is_checked_out'], result['check_out_logs'])
    return book


def delete_all():
    sql = "DELETE FROM books"
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM books WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def update(book):
    sql = "UPDATE books SET (title, genre, author_id, is_checked_out, check_out_logs) = (%s, %s, %s, %s, %s) WHERE id = %s"
    values = [book.title, book.genre, book.author.id, book.is_checked_out, book.check_out_logs, book.id]
    run_sql(sql, values)


def select_by_filter(title_search, author_search, genre_search):
    books = []

    sql = "SELECT * FROM books WHERE LOWER(title) LIKE %s AND LOWER(genre) LIKE %s"
    values = [f"%{title_search.lower()}%", f"%{genre_search.lower()}%"] 
    results = run_sql(sql, values)

    for row in results:
        author = author_repository.select(row['author_id'])
        book = Book(row['title'], row['genre'], author, row['id'], row['is_checked_out'], row['check_out_logs'])
        books.append(book)
    
    filtered_books = []
    
    for book in books:
        if not author_search:
            filtered_books.append(book)
        elif author_search.lower() in book.author.full_name().lower():
            filtered_books.append(book)

    return filtered_books
