import unittest
from models.book import Book
from models.author import Author

class TestBook(unittest.TestCase):
    
    def setUp(self):
        author = Author("Ernest", "Cline")
        self.book_1 = Book("Ready Player One", "Science Fiction", author)
    
    def test_book_has_title(self):
        self.assertEqual("Ready Player One", self.book_1.title)
    
    def test_book_has_author(self):
        self.assertEqual(self.book_1.author.first_name, "Ernest")
    
    def test_book_has_genre(self):
        self.assertEqual("Science Fiction", self.book_1.genre)

    def test_book_has_id(self):
        self.assertEqual(None, self.book_1.id)
    
    def test_update_check_out_status_to_checked_out(self):
        self.book_1.update_check_out(["checked-out"])
        self.assertEqual(True, self.book_1.is_checked_out)
    
    def test_update_check_out_status_to_checked_in(self):
        self.book_1.update_check_out(["checked-in"])
        self.assertEqual(False, self.book_1.is_checked_out)
    
    def test_new_check_out_is_logged(self):
        self.book_1.update_check_out(["checked-out"])
        self.assertEqual(len(self.book_1.check_out_logs), 1)
    