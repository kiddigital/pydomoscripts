import DomoticzEvents as DE
import subprocess as SUB
import urllib.request as URQ

sHead = "Python: TimeEvent: DomLcdBright: "
cmd = "cat /sys/class/backlight/rpi_backlight/brightness"
idx=DE.Devices["DomLcdBright"].id
curval=int(DE.Devices["DomLcdBright"].s_value)
baseurl = 'http://172.16.0.4:8080/json.htm?type=command&param=udevice'
bSucces = True

try:
# NOTE: subprocess is run as root user by Domoticz
    out = SUB.run(["rsh","root@172.16.0.251",cmd], stdout=SUB.PIPE, stderr=SUB.STDOUT, universal_newlines=True, timeout=10)
    out.check_returncode()
except:
    DE.Log(sHead + "Failed to retrieve brightness from remote screen!")
    bSucces = False

if bSucces:
    iBright = int(out.stdout)
    fPerc = (iBright/255)*100

    if fPerc > 0 and fPerc < 2:
        iPerc=1
    else:
        iPerc=int(fPerc)

    sUpdate = "No value change, no update"
    if iPerc != curval:
        url = baseurl + '&idx=' + str(idx) + '&nvalue=0&svalue=' + str(iPerc)
        with URQ.urlopen(url) as f:
            pass
        sUpdate = "Fired URL: status " + str(f.status) + ", reason " + f.reason
 
    DE.Log(sHead + "Read brightness: " + str(iBright) + ", Set brightPerc to:" + str(iPerc) + ", " + sUpdate)
