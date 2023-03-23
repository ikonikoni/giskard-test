from flask import Flask, render_template, request, jsonify

import os
import sys
import json

from millennium_falcon import odds

from celery.result import AsyncResult
import task

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
    r = { "error": 0, "id": None, "max_odd": 0, "min_day": 0 }

    # Load the empire plan
    count_down, bounty_hunter_plan = \
        odds.peep_empire_plan(request.json)

    # Find the shortest path
    shortest_path = odds.find_shortest_path(planets, \
        falcon_status[odds.DEPARTURE_KEY], falcon_status[odds.ARRIVAL_KEY])
    if len(shortest_path) == 0:
        # Failed to find a valid path
        r.update({ "max_odd": 0, "min_day": 0 })
        return r
    shortest_path_days = odds.calculate_days(shortest_path,\
        falcon_status[odds.AUTONOMY_KEY])
    if shortest_path_days > count_down:
        # Cannot arrive in time
        r.update({ "max_odd": 0, "min_day": 0 })
    else:
        # Launch the background task
        task_result = task.calculate_odds.\
            delay([], falcon_status, count_down, bounty_hunter_plan)
        r.update({\
            "id": task_result.id,\
            "min_day": shortest_path_days\
        })

    return r

@app.route('/api/retrieve-max-odd')
def retrieve_max_odd():
    if "id" not in request.args.keys():
        return { "error": 2, "odd": 0 }
    # Get the task id
    task_id = request.args["id"]

    # Construct the result
    res = AsyncResult(task_id, backend=task.app.backend)

    if res.ready():
        return { "error": 0, "odd": res.get() }
    return { "error": 1, "odd": 0 }

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
