from flask import Flask, render_template, request, jsonify

import os
import sys
import json

from millennium_falcon import odds

# Load millennium falcon status
def print_help():
    print("Usage:                                                           ")
    print("    ./app.py <millennium-falcon.json>")

global falcon_status
global planets

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
    if len(sys.argv) < 2:
        print_help()
        exit(1)

    try:
        with open(sys.argv[1], "r") as falcon_status_fd:
            # Falcon auto-check
            falcon_status = json.load(falcon_status_fd)
            if not odds.falcon_autocheck(falcon_status):
                print("Falcon auto-check failed")
                exit(1)
            
            db_path = os.path.join(os.path.dirname(sys.argv[1]),\
                falcon_status[odds.ROUTE_DB_KEY])
            # Falcon data load
            planets = odds.retrieve_falcon_db_data(db_path)
    except Exception as e:
        print("Exception:", e)
        exit(1)

    app.run(debug=True)
