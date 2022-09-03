import unittest

from Floor import Floor


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._floor = Floor(20, 30)

    def test_to_json(self):
        ecpected = "{\n\"rooms\": []\n}"
        self.assertEqual(ecpected, self._floor.toJSON())


if __name__ == '__main__':
    unittest.main()
