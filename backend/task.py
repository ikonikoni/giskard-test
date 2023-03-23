from celery import Celery
from millennium_falcon import odds

import time

# broker='pyamqp://guest@localhost//'
app = Celery('millennium_falcon_tasks',\
    backend='redis://localhost', broker="redis://localhost")

@app.task
def calculate_odds(db_results, falcon_status, count_down, bounty_hunter_plan):
    # Calculate odds
    planets = odds.construct_planets_routes(db_results)
    bf_odds = odds.brute_force_traversal(planets,\
        src_name=falcon_status[odds.DEPARTURE_KEY],\
        dst_name=falcon_status[odds.ARRIVAL_KEY],\
        autonomy=falcon_status[odds.AUTONOMY_KEY],\
        count_down=count_down,\
        bounty_hunter_plan=bounty_hunter_plan\
    )
    return bf_odds
