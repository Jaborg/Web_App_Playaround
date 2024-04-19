import os

from mock import patch

from app.crud_operations import pretty_reviews


reviews = os.listdir('tests/test_reviews/')


@patch('app.crud_operations.reviews',reviews)
def test_pretty_reviews():
    return_value = pretty_reviews()
    assert return_value == ['test review 1', 'test review 2']