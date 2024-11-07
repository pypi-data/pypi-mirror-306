import unittest
from cololog.cololog import cololog

class TestCololog(unittest.TestCase):

    def test_basic_logging(self):
        logger = cololog("test_logger", log_to_file=False)
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        self.assertTrue(True)  # Просто пример теста

if __name__ == "__main__":
    unittest.main()