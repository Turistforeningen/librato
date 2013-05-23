from datetime import datetime, timedelta
import json
import sh

from conf import *

class Sherpa():
    sherpa_metrics = None
    last_query = None
    rate = timedelta(minutes=10)

    def get_metrics(self):
        if self.sherpa_metrics is None or self.last_query <= datetime.now() - self.rate:
            self.sherpa_metrics = self.query_sherpa()
            self.last_query = datetime.now()
        return self.sherpa_metrics

    def query_sherpa(self):
        return json.loads(str(sh.Command(SHERPA_MANAGE_COMMAND)("libratometrics", _env={"PATH": SHERPA_ENV})))
