# gcair/error.py

class Error(Exception):
    """自定义异常类."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)