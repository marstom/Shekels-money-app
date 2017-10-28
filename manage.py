from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


# from shekels.db import User
from shekels.web import app, db, User, Expense

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def hello():
    print('updating')
    # Update without the need of fetching the object
    db.session.query(User).filter(User.id == 1).update({'full_name': 'dupa'})
    db.session.commit()


@manager.command
def init_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


if __name__ == "__main__":
    manager.run()
