from flask import Flask, render_template, request, jsonify

import os

from millennium_falcon import odds

app = Flask(__name__, template_folder=os.path.abspath('.'))

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(e)
        return 'Please make sure that you have run <code>npm build</code> before launching backend.'

@app.route('/api/empire-plan-uploader', methods=['POST'])
def empire_plan_uploader():
    """
    Only accept JSON file in a POST request
    """
    r = { "error": 0, "id": -1, "min_odd": 0, "min_day": 0 }
    # TODO: Calculate the shortest

    return r

# TODO: Add other endpoints

# run the application
if __name__ == "__main__":
    app.run(debug=True)
