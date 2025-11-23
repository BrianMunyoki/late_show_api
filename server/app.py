from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

#create Flask app
app=Flask(__name__)

#configureing SQLITE database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize extensions
db=SQLAlchemy(app)
migrate=Migrate(app,db)
api=Api(app)
@app.route('/')

def index():
    return("Welcome to this app")

if __name__=='__main__':
    app.run(port=5555,debug=True)