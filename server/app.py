from flask import Flask

app=Flask(__name__)

@app.route('/')

def index():
    return("Welcome to this app")

if __name__=='__main__':
    app.run(port=5555,debug=True)