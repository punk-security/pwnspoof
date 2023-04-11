from ip_handler import IPHandler

from string_formatter import handlebar_replace

import random

import secrets


class LogGenerator(object):
    dateformat = "%Y-%m-%d %H:%M:%S"
    server_ip = None
    server_fqdn = None
    log_header = {
        "IIS": "#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus sc-win32-status time-taken",
        "NGINX": "",
        "CLF": "",
        "CLOUDFLARE": "",
        "AWS": "",
    }

    # CloudFlare and AWS are missing fields normally found in their logs that would come exclusively from their respective apps e.g. AWS arn
    # This uses Cloudflare audit logs and aws elb access logs
    log_line = {
        "IIS": "{datetime} {server_ip} {method} {uri} {query} {port} {username} {source_ip} {user_agent} {referer} {status_code} {substatus} {win32_status} {time_taken}",
        "NGINX": '{source_ip} - {username} {datetime} "{method} {uri_with_query} HTTP/1.1" {status_code} {size} "{referer}" "{user_agent}"',
        "CLF": '{source_ip} - {username} {datetime} "{method} {uri_with_query} HTTP/1.1" {status_code} {size}',
        "CLOUDFLARE": '{{"ClientIP": "{source_ip}", "ClientRequestHost": "{fqdn}", "ClientRequestMethod": "{method}", "ClientRequestURI": "{uri}", "ClientRequestUserAgent":"{user_agent}", "EdgeEndTimestamp": "{datetime}", "EdgeResponseBytes": {size}, "EdgeResponseStatus": {status_code}, "EdgeStartTimestamp": "{datetime}", "RayID": "{ray_id}",  "RequestHeaders":{{"cf-access-user":"{username}"}}}}',
        "AWS": '{scheme} {datetime} app/my-loadbalancer/50dc6c495c0c9188 {source_ip}:{port} {server_ip}:{port} 0.000 0.001 0.000 {status_code} {status_code} {size} {sent_size} "{method} {scheme}://{fqdn}/{uri_with_query}:{port}/ HTTP/1.1" "{user_agent}" {https_cipher} {https_protocol} arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337262-36d228ad5d99923122bbe354" "{https_url}" "{https_cert}" 0 {datetime} "forward" "-" "-" "{server_ip}:{port}" "{status_code}" "-" "-"',
    }

    log_timeformat = {
        "IIS": "%Y-%m-%d %H:%M:%S",
        "NGINX": "[%d/%b/%Y:%H:%M:%S +0000]",
        "CLF": "[%d/%b/%Y:%H:%M:%S +0000]",
        "CLOUDFLARE": "%Y-%m-%dT%H:%M:%SZ",
        "AWS": "%Y-%m-%dT%H:%M:%SZ",
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

        # Set Referer
        if referer != "-":
            if "http" not in referer:
                scheme = "https" if port == 443 else "http"
                referer = "{scheme}://{server}/{uri}".format(
                    scheme=scheme,
                    server=LogGenerator.server_fqdn,
                    uri=referer.lstrip("/"),
                )
        else:
            scheme = "https"

        ray_id = secrets.token_hex(8)
        sent_size = random.randint(16, 1024)

        https_cipher = "-"
        https_protocol = "-"
        https_url = "-"
        https_cert = "-"
        # AWS elb access logs
        if port == 443:
            https_cipher = "ECDHE-RSA-AES128-GCM-SHA256"
            https_protocol = "TLSv1.2"
            https_url = LogGenerator.server_fqdn
            https_cert = "arn:aws:acm:us-east-2:123456789012:certificate/12345678-1234-1234-1234-123456789012"

        # Uppercase method
        method = method.upper()
        # Calc query and uri combo
        uri_with_query = "{uri}?{query}" if query != "-" else "{uri}"
        log = LogGenerator.log_line[server].format(
            datetime=datetime.strftime(LogGenerator.log_timeformat[server]),
            server_ip=LogGenerator.server_ip,
            fqdn=LogGenerator.server_fqdn,
            method=method,
            uri=uri,
            port=port,
            source_ip=source_ip,
            user_agent=user_agent,
            scheme=scheme,
            referer=referer,
            username=username,
            query=query,
            status_code=status_code,
            substatus=substatus,
            win32_status=win32_status,
            time_taken=time_taken,
            size=size_bytes,
            uri_with_query=uri_with_query.format(uri=uri, query=query),
            ray_id=ray_id,
            sent_size=sent_size,
            https_cipher=https_cipher,
            https_protocol=https_protocol,
            https_url=https_url,
            https_cert=https_cert,
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
