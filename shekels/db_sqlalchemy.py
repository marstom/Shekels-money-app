from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../expense2.db'
# To change user or password change the postgres:postres part