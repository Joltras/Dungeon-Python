import unittest

from generators.Generator import Generator


class GeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self._generator = Generator("1", "test", False)


if __name__ == '__main__':
    unittest.main()
