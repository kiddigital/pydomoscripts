import DomoticzEvents as DE

if DE.changed_device_name == "DomLcdStandBy":

    sHead = "Python: DeviceEvent: DomLcdStandBy: "

    iBrightOn = 96
    iBrightOff = 48

    if DE.is_daytime:
        iBrightOn = 192
        iBrightOff = 64

    iBrightTarget=iBrightOff

    if DE.Devices["DomLcdStandBy"].n_value_string == "Off":
        iBrightTarget=iBrightOn

    bSucces = True
    cmd = "echo " + str(iBrightTarget) + " > /sys/class/backlight/rpi_backlight/brightness"
    try:
        # NOTE: subprocess is run as root user by Domoticz
        out = SUB.run(["rsh","root@172.16.0.251",cmd], stdout=SUB.PIPE, stderr=SUB.STDOUT, universal_newlines=True, timeout=10)
        out.check_returncode()
    except:
        DE.Log(sHead + "Failed to set brightness to " + str(iBrightTarget) + " from remote screen!")
        bSucces = False

    if bSucces:
        DE.Log(sHead + "Succesfully set brightness to : " + str(iBrightTarget))
