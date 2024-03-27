import datetime
from utils.database import insert_data


def log_telemetry(data: dict, token='n/a'):
    insert_data("telemetry", {"token": token,
                "timestamp": datetime.datetime.now(), **data})
