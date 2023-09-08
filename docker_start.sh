#!/bin/ash
cd /app/ || exit 1 

python pwnspoof.py "$@" --out "${OUTPUT:-/output/pwnspoof.log}"