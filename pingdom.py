from datetime import datetime, timedelta

import requests
import json

from conf import *
from util import unix_time

# A list of probes in europa hardcoded based on pingdoms probe api output
# 09.05.2013, this might need to be synced sometimes
probes = "28,37,41,49,50,55,59,61,64,71,72,73,74,75,77,82,85,86"

# How many seconds we'll sample results for
PERIOD = 60 * 5

# Allow pingdom to process their data
offset = timedelta(seconds=(60 * 5))

# Previous measurement time
prev_utc = datetime.utcnow() - timedelta(seconds=PERIOD) - offset

def get_response_time():
    global PERIOD, offset, prev_utc

    end = datetime.utcnow() - offset
    start = end - timedelta(seconds=PERIOD)
    if start <= prev_utc:
        # We're polled more often than our check period, ignore until we're ready again
        return None

    r = requests.get(
        "%s/api/2.0/summary.average/%s" % (PINGDOM_API, PINGDOM_CHECKID),
        auth=(PINGDOM_USER, PINGDOM_PASSWORD),
        headers={'App-Key': PINGDOM_API_KEY},
        params={
            'from': unix_time(start),
            'to': unix_time(end),
            'probes': probes
        }
    )
    result = json.loads(r.text)
    if not 'summary' in result or not 'responsetime' in result['summary'] or not 'avgresponse' in result['summary']['responsetime']:
        # Some sort of error, ignore for now
        return None

    # Accept this measurement
    prev_utc = end

    # Set measure time to the middle of this measure period
    measure_time = unix_time(end - timedelta(seconds=(PERIOD / 2)))
    return {
        'name': 'sherpa.pingdom.response_time',
        'value': result['summary']['responsetime']['avgresponse'],
        'measure_time': measure_time
    }
