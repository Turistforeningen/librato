from datetime import datetime

# Sad unix time utility, see http://stackoverflow.com/questions/6999726/python-getting-millis-since-epoch-from-datetime
def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds())
