import argparse
import sys

from shekels.expense import ExpenseORMData


def gen_arg_parser():
    parser = argparse.ArgumentParser(prog='prog', description='super shekels')
    subparsers = parser.add_subparsers(prog='prog', help='sub-command help', dest='action')

    list_parser = subparsers.add_parser('list')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--name', help='name of product - need only in add', required=True)
    add_parser.add_argument('--price', help='price - needed only in add', type=int, required=True)
    return parser


def run_app(args):
    parser = gen_arg_parser()
    arguments = parser.parse_args(args)

    expense_data = ExpenseORMData('expenses.db')

    if arguments.action == 'add':
        product = {}
        product['name'] = arguments.name
        product['price'] = arguments.price
        with expense_data:
            expense_data.save(product)

    elif arguments.action == 'list':
        print("lista produktow")
        with expense_data:
            data = expense_data.load()
        print(data)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    run_app(sys.argv[1:])
