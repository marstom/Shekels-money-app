import os
import tempfile
import pytest

from shekels.expense import ExpenseCSVData, UnableToOpenDataFileException
from collections import OrderedDict


@pytest.fixture(scope='session')
def tmp_file_content():
    a = '''"name","price"
"prd",123'''
    return a


TEST_CASE_2_CONTENT = '''"name","price"
"prd1",3
"prd2",4
"prd3",13
"prd1",234
'''


def test_expense_save():
    tmp_dir = tempfile.TemporaryDirectory()

    with tmp_dir as d:
        path = os.path.join(d, 'test.csv')
        ed = ExpenseCSVData(path)
        ed.save({'name': 'a', 'price': 1})

        with open(path, 'r') as f:
            l = f.readlines()

    assert len(l) == 2


def test_expense_load(tmp_file_content):
    tmp_dir = tempfile.TemporaryDirectory()

    with tmp_dir as d:
        path = os.path.join(d, 'test.csv')

        with open(path, 'w') as f:
            f.write(tmp_file_content)

        ed = ExpenseCSVData(path)
        result = ed.load()

    assert len(result) == 1

    first_row = result[0]
    assert first_row['name'] == 'prd'
    assert first_row['price'] == 123


def test_expense_load_better(tmpdir, tmp_file_content):
    path = os.path.join(tmpdir, 'test.csv')

    with open(path, 'w') as f:
        f.write(tmp_file_content)

    ed = ExpenseCSVData(path)
    result = ed.load()

    assert len(result) == 1

    first_row = result[0]
    data = OrderedDict([('name', 'prd'),
                        ('price', 123)])

    assert data == first_row


@pytest.mark.parametrize("prd,price",
                         [
                             ('prd2', 4),
                             ('prd3', 13),
                         ]
                         )
def test_expense_search_for_product(prd, price, tmpdir):
    path = os.path.join(tmpdir, 'test.csv')
    with open(path, 'w') as f:
        f.write(TEST_CASE_2_CONTENT)

    ed = ExpenseCSVData(path)
    result = ed.search(prd)

    assert len(result) == 1

    first_row = result[0]
    data = OrderedDict([('name', prd),
                        ('price', price)])

    assert data == first_row


def test_expense_search_for_product_with_multiple_results(tmpdir):
    path = os.path.join(tmpdir, 'test.csv')
    with open(path, 'w') as f:
        f.write(TEST_CASE_2_CONTENT)

    ed = ExpenseCSVData(path)
    result = ed.search('prd1')

    assert len(result) == 2


def test_expense_save_raises_error_when_path_is_dir(tmpdir):
    path = os.path.join(tmpdir, 'test.csv')
    os.mkdir(path)

    ed = ExpenseCSVData(path)
    # This check if within with statement exception is raise.
    # Test fails if there is no exception of given type in a given block.
    with pytest.raises(UnableToOpenDataFileException):
        ed.save({'name': 'a', 'price': 1})


def test_expense_load_raises_error_when_path_is_dir(tmpdir):
    path = os.path.join(tmpdir, 'test.csv')
    os.mkdir(path)

    ed = ExpenseCSVData(path)
    with pytest.raises(UnableToOpenDataFileException):
        ed.load()


def test_expense_search_raises_error_when_path_is_dir(tmpdir):
    path = os.path.join(tmpdir, 'test.csv')
    os.mkdir(path)

    ed = ExpenseCSVData(path)
    with pytest.raises(UnableToOpenDataFileException):
        ed.search('prd1')
