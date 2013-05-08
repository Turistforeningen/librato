import time
import threading

import linux_metrics

class NetAvg(threading.Thread):

    samples_rx = []
    samples_tx = []

    def run(self):

        prev_rx = None
        prev_tx = None

        while True:
            time.sleep(1)
            rx, tx = linux_metrics.net_stat.rx_tx_bytes('eth0')

            if prev_rx is not None:
                self.samples_rx.append(rx - prev_rx)

            if prev_tx is not None:
                self.samples_tx.append(tx - prev_tx)

            prev_rx = rx
            prev_tx = tx

    def get_average(self):
        rx = None
        if len(self.samples_rx) > 0:
            rx_val = sum(self.samples_rx) / float(len(self.samples_rx))
            rx = {
                "name": "sherpa.hw.rx",
                "value": rx_val
            }
            self.samples_rx = []
        tx = None
        if len(self.samples_tx) > 0:
            tx_val = sum(self.samples_tx) / float(len(self.samples_tx))
            tx = {
                "name": "sherpa.hw.tx",
                "value": tx_val
            }
            self.samples_tx = []
        return (rx, tx)
