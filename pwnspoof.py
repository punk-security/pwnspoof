import datetime as dt
from log_generator import LogGenerator
from models import Session, SessionHandler
from apps import apps
import argparse
import sys
from session_generator import SessionGenerator, default_user_agents
import random

# TODO: build common patterns for webapps
# TODO: build attacker injector for webapp patterms
# TODO: Make noise a bit cleverer... maybe weighted wordlists?


banner = """\
         ____              __   _____                      _ __       
        / __ \__  ______  / /__/ ___/___  _______  _______(_) /___  __
       / /_/ / / / / __ \/ //_/\__ \/ _ \/ ___/ / / / ___/ / __/ / / /
      / ____/ /_/ / / / / ,<  ___/ /  __/ /__/ /_/ / /  / / /_/ /_/ / 
     /_/    \__,_/_/ /_/_/|_|/____/\___/\___/\__,_/_/  /_/\__/\__, /  
                                            PRESENTS         /____/  

                         -- PWNSpoof v0.4.0 --
  A spoof log generator to practice incident response and threat hunting!
        """

parser = argparse.ArgumentParser(
    usage="%(prog)s [options] app",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=banner,
)

parser.add_argument(
    "app",
    type=str,
    help="App to emulate",
    choices=[
        "banking",
        "wordpress",
        "generic",
    ],
)
parser.add_argument(
    "--out", type=str, default="pwnspoof.log", help="Output file (default: %(default)s)"
)

parser.add_argument(
    "--iocs",
    action="store_true",
    help="Do you want to know the attackers iocs for easier searching? (default: %(default)s)",
)
log_generator_settings = parser.add_argument_group("log generator settings")
log_generator_settings.add_argument(
    "--log-start-date",
    type=str,
    help='Initial start of logs, in the format YYYYMMDD i.e. "20210727"',
)
log_generator_settings.add_argument(
    "--log-end-date",
    type=str,
    help='End date for logs, in the format YYYYMMDD i.e. "20210727"',
)
log_generator_settings.add_argument(
    "--session-count",
    type=int,
    default=2000,
    help="Number of legitimate sessions to spoof (default: %(default)s)",
)
log_generator_settings.add_argument(
    "--max-sessions-per-user",
    type=int,
    default=3,
    help="Max number of legitimate sessions per user (default: %(default)s)",
)
log_generator_settings.add_argument(
    "--server-fqdn", type=str, help="Override the emulated web apps default fqdn"
)
log_generator_settings.add_argument(
    "--server-ip", type=str, help="Override the emulated web apps randomised IP"
)
log_generator_settings.add_argument(
    "--server-type",
    type=str,
    choices=["IIS", "NGINX", "CLF", "CLOUDFLARE", "AWS"],
    default="IIS",
    help="Server to spoof (default: %(default)s)",
)
log_generator_settings.add_argument(
    "--uri-file",
    type=str,
    help="File containing web uris to override defaults, do not include extensions",
)
log_generator_settings.add_argument(
    "--noise-file",
    type=str,
    help="File containing noise uris to override defaults, include extensions",
)
attack_settings = parser.add_argument_group("attack settings")
attack_settings.add_argument(
    "--spoofed-attacks",
    type=int,
    default=1,
    help="Number of attacker sequences to spoof (default: %(default)s)",
)
attack_settings.add_argument(
    "--attack-type",
    type=str,
    choices=["bruteforce", "command_injection"],
    default="bruteforce",
    help="Number of attacker sequences to spoof (default: %(default)s)",
)
attack_settings.add_argument(
    "--attacker-geo",
    type=str,
    default="RD",
    help="Set the attackers geo by 2 letter region.  Use RD for random (default: %(default)s)",
)
attack_settings.add_argument(
    "--attacker-user-agent",
    type=str,
    default="RD",
    help="Set the attackers user-agent.  Use RD for random (default: %(default)s)",
)
attack_settings.add_argument(
    "--additional-attacker-ips",
    type=str,
    default="",
    help="Additional attackers ip addresses, comma separated (default: %(default)s). If you wish to exclusively use this list set spoofed-attacks to 0",
)
try:
    args = parser.parse_args()
except SystemExit as e:
    parser.print_help()
    sys.exit(0)

print(banner)

# FQDN
if args.server_fqdn != None:
    LogGenerator.server_fqdn = args.server_fqdn
else:
    LogGenerator.server_fqdn = apps[args.app].fqdn

# IP
if args.server_ip != None:
    LogGenerator.server_ip = args.server_ip

# ENDDATE
if args.log_end_date != None:
    ed = dt.datetime.strptime(args.log_end_date, "%Y%m%d")
else:
    ed = dt.datetime.combine(dt.date.today(), dt.datetime.max.time())
# STARTDATE
if args.log_start_date != None:
    sd = dt.datetime.strptime(args.log_start_date, "%Y%m%d")
else:
    sd = ed - dt.timedelta(days=14)

sh = SessionHandler()
# If args.uri_file, add uris to session handler
if args.uri_file != None:
    with open(args.uri_file) as f:
        sh.pages = f.read().splitlines()
# If args.noise_file, add noise to session handler
if args.noise_file != None:
    with open(args.noise_file) as f:
        sh.noise = f.read().splitlines()

x = 0
y = 100 / args.session_count


print("Generating {} unique sessions...".format(args.session_count))
for session in SessionGenerator(
    args.session_count,
    apps[args.app],
    sd,
    ed,
    max_sessions_per_user=args.max_sessions_per_user,
):
    sh.add_session(session)
    print("{:6.2f}% ".format(y * x), end="\r", flush=True)
    x += 1
print(" Done!    ")


## Attacks - manual for now
if args.attacker_geo == "RD":
    args.attacker_geo = None

if args.attacker_user_agent == "RD":
    attacker_user_agent = random.choice(default_user_agents)
else:
    attacker_user_agent = args.attacker_user_agent

attacker_sessions = []

print("Generating {} attack sessions".format(args.spoofed_attacks))
for x in range(0, args.spoofed_attacks):
    attack_start_date = (random.choice(sh.sessions)).start_datetime
    attack = Session(
        attack_start_date,
        list(apps[args.app].attacks[args.attack_type]()),
        user_agent=attacker_user_agent,
        username=random.choice(sh.sessions).username,
        geo=args.attacker_geo,
        app=apps[args.app],
    )
    # TODO: This should be a child class of Session
    attack.attack_payloads = []
    attack.chosen_attack_payloads = []
    sh.add_session(attack)
    attacker_sessions.append(attack)

if args.additional_attacker_ips != "":
    attacker_ips = args.additional_attacker_ips.split(",")
    print("Injecting {} additional attack sessions".format(len(attacker_ips)))
    for ip in attacker_ips:
        attack_start_date = (random.choice(sh.sessions)).start_datetime
        attack = Session(
            attack_start_date,
            list(apps[args.app].attacks[args.attack_type]()),
            user_agent=attacker_user_agent,
            username=random.choice(sh.sessions).username,
            source_ip=ip,
            app=apps[args.app],
        )
        attack.attack_payloads = []
        attack.chosen_attack_payloads = []
        sh.add_session(attack)
        attacker_sessions.append(attack)
## Generate and output

print("Generating the logz and writing them to '{}'".format(args.out))
Logfile = open(args.out, "w")
print(LogGenerator.log_header[args.server_type], file=Logfile)

y = 100 / len(sh.sessions)
logs = []
while sh.active_sessions:
    for log in sh.iter(args.server_type):
        logs.append(log)
    print("{:6.2f}% ".format(100 - (y * len(sh.active_sessions))), end="\r", flush=True)
print("Writing the logs to '{}'".format(args.out))
sorted_logs = sorted(logs, key=lambda x: x["datetime"], reverse=False)
[print(log["log"], file=Logfile) for log in sorted_logs]
print(" Done!   ")
Logfile.flush()
Logfile.close()
print("Thats all Folks!")

if args.iocs:
    print("---------------iocs---------------")  #
    for attack in attacker_sessions:
        print(attack)
