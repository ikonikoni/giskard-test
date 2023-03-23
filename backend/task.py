from celery import Celery
from millennium_falcon import odds

import time

# broker='pyamqp://guest@localhost//'
app = Celery('millennium_falcon_tasks',\
    backend='redis://localhost', broker="redis://localhost")

@app.task
def calculate_odds(db_results, falcon_status, count_down, bounty_hunter_plan):
    # TODO: Calculate odds
    time.sleep(5)
    return 100
