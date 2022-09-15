import unittest

from generators.Generator import Generator


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._generator = Generator("1", "test", False)

    def test_to_json(self):
        expected = ""
        self.assertEqual(expected, self._generator.to_json())


if __name__ == '__main__':
    unittest.main()
