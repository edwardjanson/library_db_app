import unittest
from models.author import Author

class TestAuthor(unittest.TestCase):
    
    def setUp(self):
        self.author_1 = Author("Ernest", "Cline")
    
    def test_author_has_first_name(self):
        self.assertEqual("Ernest", self.author_1.first_name)
    
    def test_author_has_last_name(self):
        self.assertEqual("Cline", self.author_1.last_name)

    def test_author_has_id(self):
        self.assertEqual(None, self.author_1.id)
    
    def test_author_full_name_function(self):
        self.assertEqual("Ernest Cline", self.author_1.full_name())