from datetime import datetime

class Book:

    def __init__(self, title, genre, author, id=None, is_checked_out=False, check_out_logs=[]):
        self.title = title
        self.genre = genre
        self.author = author
        self.id = id
        self.is_checked_out = is_checked_out
        self.check_out_logs = check_out_logs
        
    
    def update_check_out(self, status):
        # Update the check-out status
        self.is_checked_out = True if "checked-out" in status else False

        # Record a new check-out log if the book is checked-out
        if self.is_checked_out:
            self.new_checkout_log()
    
    def new_checkout_log(self):
        # Add a new dated and timed check-out log
        date_time = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        self.check_out_logs.insert(0, date_time)
