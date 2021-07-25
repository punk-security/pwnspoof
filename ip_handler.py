import csv
import random
import socket
import struct


class IPHandler(object):
    ip_lookup_table = []

    @staticmethod
    def decimal_to_ip(ip):
        return socket.inet_ntoa(struct.pack(">L", ip))

    @staticmethod
    def get_random_ip(geo=None):
        if not IPHandler.ip_lookup_table:
            IPHandler.read_csv()
        candidates = IPHandler.ip_lookup_table
        if geo != None:
            candidates = [x for x in candidates if x[2] == geo.upper()]
        if len(candidates) == 0:
            raise Exception("Geo does not exist!")
        row = random.choice(candidates)
        decimal_ip = random.randint(int(row[0]), int(row[1]))
        return IPHandler.decimal_to_ip(decimal_ip)

    @staticmethod
    def read_csv():
        with open("IP2LOCATION-LITE-DB1.CSV") as file:
            c = csv.reader(file, delimiter=",", quotechar='"')
            for row in c:
                IPHandler.ip_lookup_table.append(row)
