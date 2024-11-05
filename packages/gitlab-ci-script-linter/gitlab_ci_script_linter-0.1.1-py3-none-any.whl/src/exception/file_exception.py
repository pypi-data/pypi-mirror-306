'''
Exception raised for file read errors

@author: Sydney
'''
class FileException(Exception):
    """Exception raised for file read errors"""

    def __init__(self, message, filename):
        self.message = message
        self.filename = filename
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (File name: {self.filename})"
