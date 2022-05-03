from prometheus_client import start_http_server, Summary, Counter
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
COUNT_w = Counter("total_invoke_hits", "Invoke Message ")
COUNT_p = Counter("total_prediction_hits", "Prediction Service ")
COUNT_r = Counter("total_reload_hits", "Reload Service ")

