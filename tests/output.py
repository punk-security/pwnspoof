import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from session_generator import SessionGenerator
from models import SessionHandler
import apps
import datetime


def generate_sessions(
    app,
    session_count=20,
    start_date="900821",
    end_date="900825",
    max_session_per_user=3,
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
    "NGINX": {"field_count": 12, "uri_offset": 6},
    "IIS": {"field_count": 15, "uri_offset": 4},
    "CLF": {"field_count": 10, "uri_offset": 6},
    "CLOUDFLARE": {"field_count": 21, "uri_offset": 4},
    "AWS": {"field_count": 31, "uri_offset": 14},
}


def has_double_extension(log_line, uri_offset):
    uri = log_line.split(" ")[uri_offset]
    if "?" in uri:
        # If we have params, drop them
        uri = uri.split("?")[0]
    try:
        return uri.split(".")[-1] == uri.split(".")[-2]
    except:
        return False


for application in apps.apps.keys():
    print(f"Testing {application}...")
    for log_type in log_types.keys():
        print(f"... testing log type {log_type}")
        log_uri_offset = 6
        logs = []
        sh = SessionHandler()
        for session in generate_sessions(app=apps.apps[application]):
            sh.add_session(session)
        print(f"...... got {len(sh.sessions)} sessions")
        i = 0
        while sh.active_sessions:
            for log_entry in sh.iter(log_type):
                i += 1
                # Test each log line has the correct number of whitespace seperators
                assert (
                    len(log_entry["log"].split(" "))
                    == log_types[log_type]["field_count"]
                )
                # Test each log line has no handlebars
                assert "__" not in log_entry["log"]
                # Teast eah log line has no double extensions
                assert not has_double_extension(
                    log_entry["log"], log_types[log_type]["uri_offset"]
                ), f"This log entry contains a double extension {log_entry['log']}"
        print(f"...... tested {i} log lines")
