from flask import Flask, render_template

import os

app = Flask(__name__, template_folder=os.path.abspath('.'))

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(e)
        return 'Please make sure that you have run <code>npm build</code> before launching backend.'

# TODO: Add other endpoints

# run the application
if __name__ == "__main__":
    app.run(debug=True)
