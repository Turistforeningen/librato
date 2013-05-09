import json
import time
import threading

import requests
import linux_metrics

from netavg import NetAvg
from conf import *
import pingdom

netavg = NetAvg()
netavg.start()

class Sender(threading.Thread):
    def run(self):

        metrics = {
            'gauges': [],
            'counters': []
        }

        cpu_util = 100 - linux_metrics.cpu_stat.cpu_percents(5)['idle']
        metrics['gauges'].append({
            'name': 'sherpa.hw.cpu',
            'value': cpu_util
        })

        mem_used, _, _, _, _, _ = linux_metrics.mem_stat.mem_stats()
        metrics['gauges'].append({
            'name': 'sherpa.hw.mem_usage',
            'value': mem_used
        })

        net_rx, net_tx = netavg.get_average()
        if net_rx is not None:
            metrics['gauges'].append(net_rx)
        if net_tx is not None:
            metrics['gauges'].append(net_tx)

        response_time = pingdom.get_response_time()
        if response_time is not None:
            metrics['gauges'].append(response_time)

        payload = json.dumps(metrics)

        requests.post(
            "%s/v1/metrics" % LIBRATO_API,
            auth=(LIBRATO_USERID, LIBRATO_API_TOKEN),
            headers={'Content-Type': 'application/json'},
            data=payload
        )

while True:
    Sender().start()
    time.sleep(5)
