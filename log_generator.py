from ip_handler import IPHandler

from string_formatter import handlebar_replace


class LogGenerator(object):
    dateformat = "%Y-%m-%d %H:%M:%S"
    server_ip = None
    server_fqdn = None
    log_header = {
        "IIS": "#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken",
        "NGINX": "",
        "CLF": "",
    }
    log_line = {
        "IIS": "{datetime} {server_ip} {method} {uri} {query} {port} {username} {source_ip} {user_agent} {referer} {status_code} {substatus} {win32_status} {time_taken}",
        "NGINX": '{source_ip} - {username} {datetime} "{method} {uri_with_query} HTTP/1.1" {status_code} {size} "{referer}" "{user_agent}"',
        "CLF": '{source_ip} - {username} {datetime} "{method} {uri_with_query} HTTP/1.1" {status_code} {size}',
    }
    log_timeformat = {
        "IIS": "%Y-%m-%d %H:%M:%S",
        "NGINX": "[%d/%b/%Y:%H:%M:%S +0000]",
        "CLF": "[%d/%b/%Y:%H:%M:%S +0000]",
    }

    @staticmethod
    def generate_log(
        datetime,
        uri,
        port,
        source_ip,
        user_agent,
        server,
        size_bytes,
        referer="-",
        method="get",
        username="-",
        query="-",
        status_code=200,
        substatus=0,
        win32_status=0,
        time_taken=20,
    ):
        # Format timestamp
        if LogGenerator.server_ip == None:
            LogGenerator.server_ip = IPHandler.get_random_ip(geo="US")
        if LogGenerator.server_fqdn == None:
            LogGenerator.server_fqdn = LogGenerator.server_ip
        datetime = datetime.strftime(LogGenerator.log_timeformat[server])
        # Set Referer
        if referer != "-":
            if "http" not in referer:
                scheme = "https" if port == 443 else "http"
                referer = "{scheme}://{server}/{uri}".format(
                    scheme=scheme,
                    server=LogGenerator.server_fqdn,
                    uri=referer.lstrip("/"),
                )
        # Uppercase method
        method = method.upper()
        # Calc query and uri combo
        uri_with_query = "{uri}?{query}" if query != "-" else "{uri}"
        log = LogGenerator.log_line[server].format(
            datetime=datetime,
            server_ip=LogGenerator.server_ip,
            method=method,
            uri=uri,
            port=port,
            source_ip=source_ip,
            user_agent=user_agent,
            referer=referer,
            username=username,
            query=query,
            status_code=status_code,
            substatus=substatus,
            win32_status=win32_status,
            time_taken=time_taken,
            size=size_bytes,
            uri_with_query=uri_with_query.format(uri=uri, query=query),
        )
        return log

    @staticmethod
    def map_to_log(datetime, session, interaction, server):
        referer = interaction.referer
        if referer == "__last__":
            referer = session.last_uri
        if session.authenticated:
            username = session.username
        else:
            username = "-"
        uri = handlebar_replace(interaction.uri, session)
        return LogGenerator.generate_log(
            datetime=datetime,
            uri=uri,
            port=interaction.port,
            source_ip=session.source_ip,
            user_agent=session.user_agent,
            referer=referer,
            method=interaction.method,
            query=handlebar_replace(interaction.query, session),
            status_code=interaction.status_code,
            time_taken=interaction.response_time_ms,
            username=username,
            server=server,
            size_bytes=interaction.size_bytes,
        )
