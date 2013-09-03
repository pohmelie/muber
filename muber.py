import au3bind
import os
import time
import subprocess
import math


def netstat(dst_ips, dst_ports):

    proc = subprocess.Popen("netstat -anop TCP", stdout=subprocess.PIPE)
    blob = str(bytes(filter(lambda ch: ch < 128, proc.stdout.read())), encoding="ascii")

    connections = {}

    for line in filter(bool, map(str.strip, blob.split("\n"))):

        elements = tuple(filter(bool, line.split()))

        if len(elements) == 5:

            _, src, dst, state, pid = elements
            dst_ip, dst_port = dst.split(":")

            if dst_ip in dst_ips and dst_port in dst_ports:

                connections[int(pid)] = dst_ip

    return connections


class D2Window():

    title_base = "muber"
    title_num = 1
    game_base = "muber"
    game_num = 1
    game_password = "yoba"

    timeout_exit_game = 4
    timeout_reconnect = 10

    screens = {
        "INIT":((350, 250, 450, 300), 3406352),
        "MAIN_MENU":((350, 250, 450, 300), 3876691790),
        "CONNECTION_ERROR":((250, 500, 350, 575), 2601569465),
        "LOGIN":((30, 540, 160, 580), 2060892196),
        "BAD_ACC_PASS":((30, 540, 160, 580), 836154227),
        "CHAR_SCREEN":((30, 540, 160, 580), 2171394584),
        "CREATE_GAME":((540, 450, 770, 485), 427747543),
        "IN_GAME":((0, 550, 30, 600), 4171787830),
    }

    def __init__(self, account, password, starter, au3):

        self.account = account
        self.password = password
        self.title = D2Window.title_base + str(D2Window.title_num)
        self.au3 = au3
        self.start_time = None

        D2Window.title_num += 1

        starter()
        self.au3.AU3_WinWaitActive("Diablo")
        self.pid = self.au3.AU3_WinGetProcess("Diablo")
        self.au3.AU3_WinSetTitle("Diablo", "", self.title)

        while self.au3.AU3_WinGetTitle("") != self.title:

            time.sleep(1)

        self.au3.AU3_MouseMove(10, 10)
        time.sleep(2)


    def check_rect(self, rect, rect_hash):

        return self.au3.AU3_PixelChecksum(*rect) == rect_hash


    def leave(self):

        self.send("{ESC}")
        self.click(400, 260)
        time.sleep(D2Window.timeout_exit_game)


    def send(self, txt):

        self.au3.AU3_Send(txt)


    def click(self, x, y, clicks=1, speed=0):

        self.au3.AU3_MouseClick("left", x, y, clicks, speed)
        self.au3.AU3_MouseMove(10, 10, 0)


    def join(self):

        if self.au3.AU3_WinGetTitle("") != self.title:

            self.au3.AU3_WinActivate(self.title)

        if self.check_rect(*D2Window.screens["IN_GAME"]):

            self.leave()

        while not self.check_rect(*D2Window.screens["IN_GAME"]):

            for action in D2Window.screens:

                if self.check_rect(*D2Window.screens[action]):

                    if action == "INIT":

                        self.send("{ENTER}")

                    elif action == "MAIN_MENU":

                        self.click(400, 350)

                    elif action == "CONNECTION_ERROR":

                        self.send("{ENTER}")
                        time.sleep(D2Window.timeout_reconnect)

                    elif action == "LOGIN":

                        self.click(400, 335, 2)
                        self.send(self.account + "{TAB}" + self.password + "{ENTER}")

                    elif action == "BAD_ACC_PASS":

                        return False

                    elif action == "CHAR_SCREEN":

                        self.send("{ENTER}")

                    elif action == "CREATE_GAME":

                        self.click(600, 460)
                        self.click(707, 375)
                        self.send(
                            D2Window.game_base +
                            str(D2Window.game_num) +
                            "{TAB}" +
                            D2Window.game_password +
                            "{ENTER}"
                        )
                        D2Window.game_num += 1

                    break

            time.sleep(1)

            while self.au3.AU3_WinGetTitle("") != self.title:

                time.sleep(1)

        self.start_time = time.time()
        return True


def seconds_to_human(x):

    x, s = divmod(int(x), 60)
    h, m = divmod(x, 60)
    return str.format("{:0>2}:{:0>2}:{:0>2}", h, m, s)


def muber(dst_ips, dst_ports, accounts, starter):

    timeout = 10
    games_per_ip = math.ceil(len(accounts) / len(dst_ips))
    au3 = au3bind.autoit()
    nstat = lambda: netstat(dst_ips, dst_ports)

    au3.AU3_AutoItSetOption("SendKeyDelay", 20)
    au3.AU3_AutoItSetOption("SendKeyDownDelay", 20)
    au3.AU3_AutoItSetOption("SendCapslockMode", 0)
    au3.AU3_AutoItSetOption("WinTitleMatchMode", 2)
    au3.AU3_AutoItSetOption("MouseClickDownDelay", 25)
    au3.AU3_AutoItSetOption("MouseCoordMode", 2)
    au3.AU3_AutoItSetOption("PixelCoordMode", 2)

    wins = []
    for account, password in accounts:

        wins.append(D2Window(account, password, starter, au3))

    while True:

        ns = nstat()
        badwins = []

        for win in wins:

            if win.pid not in ns:

                if win.start_time:

                    print(
                        str.format(
                            "*{} dropped after {}",
                            win.account,
                            seconds_to_human(time.time() - win.start_time)
                        )
                    )

                while win.join():

                    ns = nstat()

                    if tuple(ns.values()).count(ns[win.pid]) <= games_per_ip:

                        print(str.format("*{} -> {}", win.account, ns[win.pid]))
                        break

                else:

                    badwins.append(win)
                    print(str.format("*{} wrong acc or pass", win.account))

        wins = list(filter(lambda w: w not in badwins, wins))
        time.sleep(timeout)


if __name__ == "__main__":

    dst_ips = ("212.42.38.182", "212.42.38.174", "212.42.38.87")
    dst_ports = ("4000",)
    accounts = tuple(map(lambda line: line.strip().split("/"), open("accounts.txt")))

    muber(dst_ips, dst_ports, accounts, lambda: os.startfile("d2.lnk"))
