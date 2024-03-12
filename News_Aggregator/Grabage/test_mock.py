import unittest
from sample_mock import len_joke, get_joke, add_numbers
from unittest.mock import patch, MagicMock


class TestJoke(unittest.TestCase):
    @patch("sample_mock.get_joke")
    def test_len_joke(self, mock_get_joke):
        mock_get_joke.return_value = 'one'
        self.assertEqual(len_joke(), 3)

    @patch("sample_mock.requests")
    def test_get_joke(self, mock_req):
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_req.get.return_value = mock_response
        self.assertEqual(get_joke(), 'No Jokes')
        mock_response.status_code = 200
        mock_response.json.return_value = {'value': {'jokes': 'one'}}
        self.assertEqual(get_joke(), 'one')

    @patch("sample_mock.get_numbers")
    def test_add_numbers(self, mock_get_numbers):
        mock_get_numbers.return_value = [2, 3]
        self.assertEqual(add_numbers(), 5)

