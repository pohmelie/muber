import subprocess
import collections


def netstat():

    proc = subprocess.Popen("netstat -ano", stdout=subprocess.PIPE)
    blob = str(bytes(filter(lambda ch: ch < 128, proc.stdout.read())), encoding="ascii")
    lines = tuple(filter(bool, blob.split("\n")))
    structured_lines = tuple(map(lambda l: tuple(filter(bool, l.strip().split())), lines))
    connections = tuple(filter(lambda sl: len(sl) >= 5, structured_lines))
    tcp = tuple(filter(lambda sl: sl[0] == "TCP", connections))

    return tcp



for yoba in netstat():

    print(yoba)
