"""
This file contains the test cases for the generator class.
"""
import unittest

from generators.generator import Generator


class GeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self._generator = Generator("1", "test", False)


if __name__ == "__main__":
    unittest.main()
