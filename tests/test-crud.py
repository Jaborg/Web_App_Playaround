import os
from unittest.mock import patch
from app.crud import pretty_reviews

def test_pretty_reviews():
    """Test the pretty_reviews function to ensure it formats review titles correctly."""
    with patch('os.listdir', return_value=['test-review-1.html', 'test-review-2.html', 'images']):
        return_value = pretty_reviews()
        assert return_value == ['test review 1', 'test review 2']