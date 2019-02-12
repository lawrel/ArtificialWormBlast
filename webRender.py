from flask import Flask, render_template
app = Flask(__name__)



#Functions defining the pages
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lobby/')
def lobby():
    return render_template('lobby.html')

@app.route('/myAccount/')
def myAccount():
    return render_template('Account.html')

@app.route('/Instructions/')
def Instructions():
    return render_template('Instructions.html')


if __name__ == '__main__':
    app.run(debug = True)
    print ("DID THE THING.")

    