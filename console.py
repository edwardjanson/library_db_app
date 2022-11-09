import pdb
from models.book import Book
from models.author import Author

import repositories.book_repository as book_repository
import repositories.author_repository as author_repository

author_repository.delete_all()
book_repository.delete_all()

author1 = Author("Stephen", "King")
author_repository.save(author1)
author2 = Author("George", "Orwell")
author_repository.save(author2)

author_repository.select_all()

book_1 = Book("The Shining", "Horror", author1)
book_repository.save(book_1)

book_2 = Book("Animal Farm", "Satire", author2)
book_repository.save(book_2)

books = book_repository.select_all()

pdb.set_trace()
