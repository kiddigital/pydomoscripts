import DomoticzEvents as DE

SCRIPT = 'nadserial.py' 
DEVICE = 'root@172.16.0.252'
LEVEL0 = 'Off'
LEVEL1 = 'Achtergrond'
LEVEL2 = 'Zachtjes'
LEVEL3 = 'Luisteren'
STREAMER = '9'
COAXIN = '5'

def talk_to_nad(cmd=None):
    if cmd is None:
        return False

    cmd='./' + SCRIPT + ' ' + cmd
    try:
        # NOTE: subprocess is run as root user by Domoticz
        out = SUB.run(["rsh",DEVICE,cmd], stdout=SUB.PIPE, stderr=SUB.STDOUT, universal_newlines=True, timeout=10)
        out.check_returncode()
    except:
        return False

    ret = out.stdout.rstrip('\r\n')
    ret = ret.split('=',maxsplit=1)
    if len(ret) == 2:
        return ret[1]
    return ret[0]

def set_volume(vol=-72):
    iNewVolume = int(vol)
    if iNewVolume <= -20 and iNewVolume >= -72:
        sCurVolume = talk_to_nad('Main.Volume='+str(iNewVolume))
        if int(sCurVolume) != iNewVolume:
            return False
    else:
        return False
    return int(sCurVolume)

if DE.changed_device_name == "Muziek":

    sHead = "Python: DeviceEvent: Muziek: "
    bContinue = True
    sValue = None
    sCurPower = None
    sCurSource = None
    sCurVolume = None

    sValue=DE.Devices["Muziek"].n_value_string
    sCurPower=talk_to_nad('Main.Power?')
    sCurVolume=talk_to_nad('Main.Volume?')
    sCurSource=talk_to_nad('Main.Source?')
    sNewPower = sCurPower
    sNewVolume = sCurVolume
    sNewSource = sCurSource

    if (sCurPower == False or sCurVolume == False or sCurSource == False):
        DE.Log(sHead + "Failed to communicate succesfully with NAD! ")
        bContinue = False
    else:
        if sValue == LEVEL0:
            #DE.Log('Turning Off')
            sNewPower = 'Off'
            sNewVolume = '-72'
            sNewSource = COAXIN
        elif sValue == LEVEL1:
            #DE.Log('Achtergrond On')
            sNewPower = 'On'
            sNewVolume = '-60'
            sNewSource = STREAMER
        elif sValue == LEVEL2:
            #DE.Log('Zachtjes On')
            sNewPower = 'On'
            sNewVolume = '-50'
            sNewSource = STREAMER
        elif sValue == LEVEL3:
            #DE.Log('Luisteren On')
            sNewPower = 'On'
            sNewVolume = '-40'
            sNewSource = STREAMER
        else:
            DE.Log(sHead + 'Unknown level ' + sValue)

    if sNewVolume != sCurVolume and bContinue:
       iNewVolume = set_volume(sNewVolume)
       if iNewVolume == False:
           DE.Log(sHead + 'Setting Volume failed!')
           bContinue = False
       else:
           sNewVolume=str(iNewVolume)

    if sNewPower != sCurPower and bContinue:
        sCurPower = talk_to_nad('Main.Power='+sNewPower)
        if sCurPower != sNewPower:
            DE.Log(sHead + 'Turning Power on/off failed!')
            bContinue = False
        else:
            if sCurPower == 'On':
                sCurSource = talk_to_nad('Main.Source='+COAXIN)

    if sNewSource != sCurSource and bContinue:
        sCurSource = talk_to_nad('Main.Source='+sNewSource)
        if sCurSource != sNewSource:
            DE.Log(sHead + 'Setting Source failed!')
            bContinue = False

    DE.Log(sHead + 'NAD set to ' + sCurPower + ', Volume: ' + sCurVolume + ', Source: ' + sCurSource)
