import csv
import os
import sqlite3
from collections import OrderedDict

from shekels.db import DB, Expense


class MyDialect(csv.unix_dialect):
    quoting = csv.QUOTE_NONNUMERIC


class UnableToOpenDataFileException(Exception):
    pass


class ExpenseSQLData:
    def __init__(self, file_name):
        self._file_name = file_name
        self._connection = None

    def __enter__(self):
        self._connection = sqlite3.connect(self._file_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def save(self, product):
        cursor = self._connection.cursor()
        query = "insert into expense ('name', 'price')" \
                "values ('{name}', {price})".format(**product)
        cursor.execute(query)
        self._connection.commit()

    def load(self):
        cursor = self._connection.cursor()
        query = "SELECT name, price FROM expense"
        query_result = cursor.execute(query)
        result = []
        for row in query_result:
            result.append(OrderedDict([
                ('name', row[0]),
                ('price', row[1]),
            ]))
        return result


class ExpenseCSVData:
    def __init__(self, file_name):
        self._file_name = file_name
        self._field_names = ['name', 'price']

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, product):
        """
        Save product in CSV file
        :param product: dict with product details
        :return: None
        """
        self._check_path()
        exists = os.path.exists(self._file_name)

        with open(self._file_name, 'a') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self._field_names,
                dialect=MyDialect)

            if not exists:
                writer.writeheader()
            writer.writerow(product)

    def _check_path(self):
        if os.path.isdir(self._file_name):
            raise UnableToOpenDataFileException("Path is a directory")

    def load(self):
        self._check_path()
        result = []
        with open(self._file_name, 'r') as csvfile:
            reader = csv.DictReader(
                csvfile,
                dialect=MyDialect)

            for row in reader:
                result.append(row)

        return result

    def search(self, product_name):
        self._check_path()
        result = []
        with open(self._file_name, 'r') as csvfile:
            reader = csv.DictReader(
                csvfile,
                dialect=MyDialect)

            for row in reader:
                if row['name'] == product_name:
                    result.append(row)

        return result


class ExpenseORMData:
    def __init__(self, file_name):
        self._db = DB(file_name)

    def __enter__(self):
        self._session = self._db.get_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def save(self, product):
        e = Expense(name=product['name'], price=product['price'])
        self._session.add(e)
        self._session.commit()

    def load(self):
        expenses = self._session.query(Expense).all()
        expense_list = []
        for e in expenses:
            expense_list.append({
                'name': e.name,
                'price': e.price
            })

        return expense_list
