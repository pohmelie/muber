import au3bind
import os
import time
import subprocess
import ctypes


au3 = au3bind.autoit()

au3.AU3_AutoItSetOption("SendKeyDelay", 20)
au3.AU3_AutoItSetOption("SendKeyDownDelay", 20)
au3.AU3_AutoItSetOption("SendCapslockMode", 0)
au3.AU3_AutoItSetOption("WinTitleMatchMode", 2)
au3.AU3_AutoItSetOption("MouseClickDownDelay", 25)
au3.AU3_AutoItSetOption("MouseCoordMode", 2)
au3.AU3_AutoItSetOption("PixelCoordMode", 2)

#print(subprocess.call("netstat -ano"))
#exit()

os.startfile("d2.lnk")
au3.AU3_WinWaitActive("Diablo")
print(au3.AU3_WinGetProcess("Diablo", ""))
print(au3.AU3_WinGetTitle("", ""))
au3.AU3_MouseMove(-100, -100, 0)
exit()

while True:

    print(au3.AU3_PixelChecksum(350, 250, 450, 300))
    time.sleep(1)
