# Shekels - super money app!(Tutorial flask project)
This will be app for home expenses. App is in development.

### Features:
* Commandline CLI
* Web abb in flask
* Register user
* Login user
* Add bootstrap to html

## Used libraries

* csv: https://docs.python.org/3.5/library/csv.html
* argparse: https://docs.python.org/3.5/library/argparse.html
* pytest: https://docs.pytest.org/en/latest/
* pytest fixtures: https://docs.pytest.org/en/latest/fixture.html

# install postgres on linux

https://help.ubuntu.com/community/PostgreSQL

sudo apt-get install postgresql

Install postgres client:
sudo apt-get install postgresql-client

marstom@marstom-X55VD /usr/local $ psql
marstom@marstom-X55VD /usr/local $ sudo su - postgres

# how to run...

python manage.py db init
python manage.py migrate
python manage.py upgrade -if you make changes in db