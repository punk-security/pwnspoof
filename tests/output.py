import os
from random import randint
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from session_generator import SessionGenerator
from models import ActivityPattern, SessionHandler
import apps
import datetime


def generate_sessions(
    session_count=10,
    start_date="900821",
    end_date="900825",
    max_session_per_user=3,
    app=apps.apps["banking"],
):
    sd = datetime.datetime.strptime(start_date, "%Y%m%d")
    ed = datetime.datetime.strptime(end_date, "%Y%m%d")
    return SessionGenerator(
        session_count,
        app,
        sd,
        ed,
        max_sessions_per_user=max_session_per_user,
    )


log_types = {
    "NGINX": 12,
    "IIS": 15,
    "CLF": 10,
}

for application in apps.apps.values():
    for log_type in log_types.keys():
        logs = []
        sh = SessionHandler()
        for session in generate_sessions(app=application):
            sh.add_session(session)
        while sh.active_sessions:
            for log_entry in sh.iter(log_type):
                # Test each log line has the correct number of whitespace seperators
                assert len(log_entry["log"].split(" ")) == log_types[log_type]
                # Test each log line has no handlebars
                assert "__" not in log_entry["log"]
