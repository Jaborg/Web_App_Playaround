import os

from mock import patch


from  ..app.crud_operations import (read_reviews_crud,)

reviews = os.listdir('app/templates/reviews')


@patch('app.crud_operations.reviews',reviews)
def test_read_reviews_curd():
    return_value = read_reviews_crud()
    assert return_value == reviews