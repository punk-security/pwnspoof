import datetime as dt
import random
from string_formatter import handlebar_replace
from ip_handler import IPHandler
from log_generator import LogGenerator
from copy import copy


class SessionHandler(object):
    def __init__(self, pages=None, noise=None):
        self.sessions = []
        self.pages = pages
        self.noise = noise

    def add_session(self, session):
        session.pages = self.pages
        session.noise = self.noise
        self.sessions.append(session)

    @property
    def active_sessions(self):
        return [x for x in self.sessions if x.next_iteration != None]

    def iter(self, server_type):
        for session in self.active_sessions:
            ni = session.next_iteration
            ret = session.trigger(ni)
            if ret != None:
                for i in ret:
                    yield {
                        "datetime": ni,
                        "log": LogGenerator.map_to_log(ni, session, i, server_type),
                    }


class Session(object):
    def __init__(
        self,
        start_datetime,
        activity_patterns,
        user_agent,
        app,
        source_ip=None,
        geo="GB",
        duration_mins=30,
        username="-",
        theme=None,
        pages=None,
        noise=None,
    ):
        if source_ip:
            self.source_ip = source_ip
        else:
            self.source_ip = IPHandler.get_random_ip(geo)
        self.start_datetime = start_datetime
        self.end_datetime = start_datetime + dt.timedelta(minutes=duration_mins)
        self.activity_patterns = []
        for ap in activity_patterns:
            if type(ap) is list:
                for ap2 in ap:
                    self.activity_patterns.append(ap2)
            else:
                self.activity_patterns.append(ap)
        self.user_agent = user_agent
        self.username = username
        self.next_iteration = start_datetime
        self.current_activity_pattern = 0
        self.current_uri = "-"
        self.last_uri = "-"
        self.iter = 0
        self.authenticated = False
        self.app = app
        self.stickystr = False
        self.geo = geo
        self.theme = theme
        self.pages = pages
        self.noise = noise

    def trigger(self, datetime):
        self.last_uri = self.current_uri
        self.last_trigger = datetime
        resp = self.activity_patterns[self.current_activity_pattern].iterate(self.iter)
        self.iter += 1
        if resp == None:
            # Activity Pattern finished, move to next one or return None
            if len(self.activity_patterns) - 1 == self.current_activity_pattern:
                self.next_iteration = None
                # Last pattern, return None
                return None
            self.current_activity_pattern += 1
            self.iter = 0
            resp = self.activity_patterns[self.current_activity_pattern].iterate(
                self.iter
            )
            self.iter += 1
        if resp != None:
            # Format the URI here so the last uri is correct - have to copy otherwise we replace uri on the base interaction
            resp = copy(resp)
            resp.uri = handlebar_replace(resp.uri, self)
            if resp.set_as_last == True:
                self.current_uri = resp.uri
            if resp.login == True:
                self.authenticated = True
            if resp.logout == True:
                self.authenticated = False
        self.next_iteration = datetime + dt.timedelta(
            seconds=random.randint(
                self.activity_patterns[
                    self.current_activity_pattern
                ].min_period_between_invocations_s,
                self.activity_patterns[
                    self.current_activity_pattern
                ].max_period_between_invocations_s,
            )
        )
        if self.next_iteration > self.end_datetime:
            self.next_iteration = None
        ### Yield noise
        # TODO: add noise suppression for api abuse
        if (
            resp != None
            and self.app.noise_interactions
            and self.activity_patterns[self.current_activity_pattern].suppress_noise
            == False
        ):
            for x in range(1, random.randint(2, 4)):
                yield random.choice(self.app.noise_interactions)
        yield resp
        return


class ActivityPattern(object):
    def __init__(
        self,
        looping=False,
        consecutive=False,
        min_period_between_invocations_s=3,
        max_period_between_invocations_s=30,
        count=None,
        suppress_noise=False,
    ):
        self.looping = looping
        self.consecutive = consecutive
        self.min_period_between_invocations_s = min_period_between_invocations_s
        self.max_period_between_invocations_s = max_period_between_invocations_s
        self.interactions = []
        self.count = count
        self.suppress_noise = suppress_noise

    def add_interaction(self, interaction):
        self.interactions.append(interaction)
        return self

    def add_interactions(self, interactions):
        for i in interactions:
            self.add_interaction(i)
        return self

    def iterate(self, iteration):
        # If random
        if self.consecutive == False:
            i = random.randint(0, len(self.interactions) - 1)
            # If there is a count, return none once we exceed it
            if self.count != None and iteration >= self.count:
                return None
        # else we are consecutive
        else:
            if iteration == len(self.interactions):
                # We have finished, return None
                return None
            i = iteration
        return self.interactions[i]


class Interaction(object):
    def __init__(
        self,
        uri,
        method="GET",
        query="-",
        referer="__last__",
        status_code=200,
        port=443,
        base_response_time_ms=25,
        response_time_deviation_ms=5,
        average_bytes=250,
        deviation_bytes=120,
        set_as_last=True,
        login=False,
        logout=False,
        append_extension=True,
    ):
        self.uri = uri.rstrip("?")
        if append_extension:
            self.uri = f"{self.uri}__app_extension__"
        self.base_response_time_ms = base_response_time_ms
        self.response_time_deviation_ms = response_time_deviation_ms
        self.average_bytes = average_bytes
        self.deviation_bytes = deviation_bytes
        self.method = method
        self.query = query.lstrip("?")
        self.referer = referer
        self.status_code = status_code
        self.port = port
        self.current_int = 0
        self.set_as_last = set_as_last
        self.login = login
        self.logout = logout

    @property
    def response_time_ms(self):
        return random.randint(
            self.base_response_time_ms - self.response_time_deviation_ms,
            self.base_response_time_ms + self.response_time_deviation_ms,
        )

    @property
    def size_bytes(self):
        return random.randint(
            self.average_bytes - self.deviation_bytes,
            self.average_bytes + self.deviation_bytes,
        )


class App(object):
    def __init__(self, fqdn):
        self.fqdn = fqdn
        self.__activity_patterns = []
        self.attacks = {}
        self.noise_interactions = []
        self.extension = "php"

    ## Activity Patterns
    def add_activity_pattern(self, ap):
        self.activity_patterns.append(ap)

    def add_activity_patterns(self, aps):
        for ap in aps:
            self.__activity_patterns.append(ap)

    def set_dynamic_activity_pattern(self, dap):
        self.dynamic_activity_pattern = dap

    def activity_patterns(self):
        if not self.dynamic_activity_pattern:
            for ap in self.__activity_patterns:
                yield ap
        else:
            for ap in self.dynamic_activity_pattern():
                yield ap
