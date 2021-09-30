import os
from random import randint
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from session_generator import SessionGenerator
from models import SessionHandler
from apps import banking
import datetime
import numpy

# def SessionGenerator(
#    num_sessions,
#    app,
#    start_date,
#    end_date,
#    average_duration_mins=30,
#    duration_deviation_mins=5,
#    user_agents=default_user_agents,
#    geos=default_geos,
#    hour_profile=hour_profile,
#    max_sessions_per_user=5,
# ):

### Test Sessions


def generate_sessions(
    session_count=100,
    start_date="900821",
    end_date="900825",
    max_session_per_user=3,
):
    sd = datetime.datetime.strptime(start_date, "%Y%m%d")
    ed = datetime.datetime.strptime(end_date, "%Y%m%d")
    return SessionGenerator(
        session_count,
        banking,
        sd,
        ed,
        max_sessions_per_user=max_session_per_user,
    )


session_length_tests = [10, 20, 50, 100]
max_sessions_per_user_tests = [1, 3, 5, 10]

# Test session count matches up

for session_count in session_length_tests:
    for max_sessions_per_user in max_sessions_per_user_tests:
        sessions = list(
            generate_sessions(
                session_count=session_count,
                max_session_per_user=max_sessions_per_user,
            )
        )
        lower_bound = session_count - max_sessions_per_user
        upper_bound = session_count + max_sessions_per_user
        print(
            f"testing session counts - SESSION COUNT:'{session_count}'  SESSIONS PER USER: '{max_sessions_per_user}'"
        )
        print(
            f"... we have '{len(sessions)}' sessions which should be between {lower_bound} and {upper_bound}"
        )
        assert lower_bound <= len(sessions) <= upper_bound
        if max_sessions_per_user > 1 and session_count / max_sessions_per_user > 2:
            source_ips = list(x.source_ip for x in sessions)
            source_ips_count = len(list(dict.fromkeys(source_ips)))
            average_sessions_per_user = max_sessions_per_user / 2
            ideal_source_ip_count = session_count / average_sessions_per_user
            print(
                f"... we have {source_ips_count} unique source IPs, and should have around {ideal_source_ip_count:.0f}"
            )
            assert (
                ideal_source_ip_count * 0.5
                < source_ips_count
                < ideal_source_ip_count * 1.5
            )


# Test session timestamp generation and spread

log_window_days_tests = [1, 2, 4, 8, 16, 32, 200]


def session_start(e):
    return e.start_datetime


for log_windows_days in log_window_days_tests:
    y = randint(1960, 2160)
    m = randint(1, 12)
    d = randint(1, 28)
    sd = f"{y}{m:02d}{d:02d}"
    sdt = datetime.datetime.strptime(sd, "%Y%m%d")
    edt = sdt + datetime.timedelta(days=log_windows_days)
    ed = edt.strftime("%Y%m%d")
    sc = 50
    sessions = list(generate_sessions(start_date=sd, end_date=ed, session_count=sc))
    sessions.sort(key=lambda e: e.start_datetime)
    print(f"testing session population - sessions should start between {sd} and {ed} ")
    print(
        f"... earliest session is {sessions[0].start_datetime} and latest is {sessions[-1].start_datetime}"
    )
    # Earliest session is after the start date
    assert sessions[0].start_datetime >= sdt
    # Latest session starts before the requested end
    assert sessions[-1].start_datetime <= edt
    start_times = list(
        (x.start_datetime.timestamp() - sdt.timestamp()) for x in sessions
    )
    target_deviation_s = (
        (log_windows_days) * 24 * 60 * 60
    ) / 4  # 4 being halfway to halfway (which is mean)
    deviation_s = numpy.std(start_times)
    print(
        f"... session start time deviation is {deviation_s:.0f} and should be {target_deviation_s:.0f} which is factor difference of {deviation_s / target_deviation_s:.2f}"
    )
    assert 0.5 < (deviation_s / target_deviation_s) < 1.5
