# test_calculator.py

import unittest
from unittest.mock import MagicMock
from calculator import add


class TestCalculator(unittest.TestCase):
    def test_add(self):
        # Create a MagicMock object to mock the add function
        mock_add = MagicMock()

        # Patch the add function with the MagicMock object
        with unittest.mock.patch('calculator.add', mock_add):
            # Call the function under test
            result = add(3, 4)

            # Assert that the add function was called with the correct arguments
            mock_add.assert_called_once_with(3, 4)

            # Assert the result
            self.assertEqual(result, 7)


if __name__ == '__main__':
    unittest.main()
