[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/punk-security/pwnspoof/graphs/commit-activity)
[![Maintainer](https://img.shields.io/badge/maintainer-PunkSecurity-blue)](https://www.punksecurity.co.uk)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=punk-security_pwnspoof&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=punk-security_pwnspoof)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=punk-security_pwnspoof&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=punk-security_pwnspoof)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=punk-security_pwnspoof&metric=bugs)](https://sonarcloud.io/summary/new_code?id=punk-security_pwnspoof)

[![Logo](/images/banner.png)](#)

pwnSpoof (from [Punk Security](https://punksecurity.co.uk/)) generates realistic spoofed log files for common web servers with customisable attack scenarios.

Every log bundle is unique and completely customisable, making it perfect for generating CTF scenarios and for training serials.

Can you find the attacker session and build the incident picture?

[![realistic_activity](/images/realistic_patterns.png)](#)

## Table of Contents

*  [About The Project     ](#About-The-Project)
*  [Getting Started       ](#Getting-Started)
    *  [Prerequisites     ](#Prerequisites)
    *  [Installation      ](#Installation)
*  [Usage                 ](#Usage)
    *  [Switches          ](#Switches)
    *  [Example           ](#Examples)
*  [View Demo             ](#Demo)
*  [Road Map              ](#Road-Map)
*  [Contact               ](#Contact)

## About The Project

pwnSpoof was created on the back of a threat hunting training exercise [Punk Security](https://punksecurity.co.uk) delivered for a customer.  The training exercise was to use a log analytic tool such as Splunk (other log analysing tools are available) and IIS logs to find login brute-force attacks and command injections.

The idea behind the pwnSpoof application is to;
*  Provide a quick CTF style training environment
*  Create unique logs every run
*  Test threat hunting in IIS, Apache, NGINX, Cloudflare and AWS ALB logs

Once you have created a set of logs, the idea is to load them in to Splunk and use various techniques to answer the following questions;

*  What was the attackers IP address and user_agent?
*  Did the attacker authenticate and if so, with what account?
*  Where was geo-location of the attacker?
*  When did the attack occur?
*  What kind of attack was it?
*  What happened during the attack?
*  What artifacts may remain on the server?
*  What steps can be taken to remediate?

## Getting Started

The following will explain how to get started with pwnSpoof

### Prerequisites

pwnSpoof is written in python and is tested with python3.   No extra modules are needed, we only use the standard library.

If you get the following error message, please specifiy python3 when running pwnSpoof.  Python2 is not supported.

```
  File "pwnspoof.py", line 176
    print("{:6.2f}% ".format(y * x), end="\r", flush=True)
                                        ^
SyntaxError: invalid syntax
```

### Installation

1. Git clone the pwnSpoof repo

```
git clone https://github.com/punk-security/pwnspoof
```

2. change directory to pwnSpoof

```
cd pwnspoof
```

3. Run pwnSpoof

```
python pwnspoof.py --help
```

## Usage
### Switches

```
positional arguments:
  {banking,wordpress,generic}
                        App to emulate

options:
  -h, --help            show this help message and exit
  --out OUT             Output file (default: pwnspoof.log)
  --iocs                Do you want to know the attackers iocs for easier searching? (default: False)

log generator settings:
  --log-start-date LOG_START_DATE
                        Initial start of logs, in the format YYYYMMDD i.e. "20210727"
  --log-end-date LOG_END_DATE
                        End date for logs, in the format YYYYMMDD i.e. "20210727"
  --session-count SESSION_COUNT
                        Number of legitimate sessions to spoof (default: 2000)
  --max-sessions-per-user MAX_SESSIONS_PER_USER
                        Max number of legitimate sessions per user (default: 3)
  --server-fqdn SERVER_FQDN
                        Override the emulated web apps default fqdn
  --server-ip SERVER_IP
                        Override the emulated web apps randomised IP
  --server-type {IIS,NGINX,CLF,CLOUDFLARE,AWS}
                        Server to spoof (default: IIS)
  --uri-file URI_FILE   File containing web uris to override defaults, do not include extensions
  --noise-file NOISE_FILE
                        File containing noise uris to override defaults, include extensions

attack settings:
  --spoofed-attacks SPOOFED_ATTACKS
                        Number of attacker sequences to spoof (default: 1)
  --attack-type {bruteforce,command_injection}
                        Number of attacker sequences to spoof (default: bruteforce)
  --attacker-geo ATTACKER_GEO
                        Set the attackers geo by 2 letter region. Use RD for random (default: RD)
  --attacker-user-agent ATTACKER_USER_AGENT
                        Set the attackers user-agent. Use RD for random (default: RD)
  --additional-attacker-ips ADDITIONAL_ATTACKER_IPS
                        Additional attackers ip addresses, comma separated (default: ). If you wish to exclusively use this list set spoofed-attacks to 0
```

### Examples

The following example will create a set of IIS logs for bruteforce against pwnedbank.co.uk.

```
python pwnspoof.py banking --server-fqdn pwnedbank.co.uk --attack-type bruteforce --server-type IIS --out iis-output.log
```

The following example will create a set of NGINX logs for command_injection against pwnedbank.co.uk.

```
python pwnspoof.py banking --server-fqdn pwnedbank.co.uk --attack-type command_injection --server-type NGINX
```

The following example will create a set of logs with 5000 routine sessions and 3 attack sessions

```
python pwnspoof.py banking --session-count 5000 --spoofed-attacks 3
```

The following example will create a set of logs and output the attackers IP addresses

```
python pwnspoof.py banking --spoofed-attacks 3 --iocs 
```

The following example will create a set of logs and exclusively use the IP addresses specified

```
python pwnspoof.py banking --spoofed-attacks 0 --additional-attacker-ips 192.168.0.1,192.168.0.2
```

## Demo

[![Demo](/images/pwnspoof.gif)](#Demo)

## Road Map

pwnSpoof is built to produce to authentic web attack logs and it does this really well.  Right now we are focused on refactoring the code, building out our testing suite and getting the first push to PyPi but we have *huge* ambitions for pwnSpoof.

### Coming soon
Adding extra webapps beyond banking to provide extra variety to the logs

*  Social media
*  Wordpress
*  E-Commerce

Adding additional and more dynamic web attacks

*  Full OWASP TOP 10
*  Customisable payload encoding
*  Multi-session attacks
*  Obfuscation 

### Unscheduled aspirations
**Training Videos!**

pwnSpoof was built to be a great tool for training the blue team so it only makes sense to produce some training materials to show it off.

*  How to ingest logs in to various log analyser (Splunk, Elastic, Open Disto, Sentinel)
*  How to use the power of REGEX to pivot around the data

**Not just weblogs**

We would love to see pwnSpoof generating all kinds of threat hunting logs such as Office365 audit logs for Sharepoint, Onedrive and AzureAD

**Blackhat Arsenal**

We have submitted pwnSpoof to Blackhat Arsenal for consideration and it would be AWESOME to demo it at Blackhat London this year (2021).

**Why not contact us with some extra ideas, or add to the project**

## Contact

* Simon Gurney        - simon.gurney@punksecurity.co.uk
* Daniel Oates-Lee    - daniel.oates-lee@punksecurity.co.uk

## Credit

* **ip2location** :
We make use of the IP2Location LITE Country database to provide geographically relevant IP addresses.

This product includes IP2Location LITE data available from [https://lite.ip2location.com](https://lite.ip2location.com)
