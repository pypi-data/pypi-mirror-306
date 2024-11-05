#!/usr/bin/env python3
# vim: set fenc=utf-8 ts=4 sw=0 sts=0 sr et si tw=0 fdm=marker fmr={{{,}}}:

# {{{ Imports
import pydbus
from gi.repository import GLib
# }}}

# {{{ Variables
# {{{ Basic
sysBus        = pydbus.SystemBus()
upowerBusName = "org.freedesktop.UPower"
# }}}

# {{{ Initialize global variables
notiMsg   = { }
lastState = 0
# }}}

# {{{ Get battery path
upowerObject  = sysBus.get(upowerBusName, "/org/freedesktop/UPower")
upowerDevices = upowerObject.EnumerateDevices()

for devicePath in upowerDevices:                # go through all devices on dbus from upower
    bat = sysBus.get(upowerBusName, devicePath) # create a device to test its properties
    if bat.Type == 2:                           # if "Type" property is `2` (`"Battery"`)
        if bat.PowerSupply:                     # if "PowerSupply" property is `True`
            batteryPath = devicePath            # set battery path to that device path
# }}}
# }}}

# {{{ Functions
# {{{ Convert seconds to time remaining
def convertSeconds(totalSeconds):
    hours,   remainder = divmod(totalSeconds, 3600)
    minutes, seconds   = divmod(remainder, 60)
    return f"{int(hours)} h {int(minutes)} min"
# }}}

# {{{ Refresh notifications
def refreshNotif(which):
    global notiMsg

    match which:
        # {{{ Fully charged
        case "Charged":
            notiMsg["Charged"] = {
                "appName":  "Battery",
                "title":    "Fully charged",
                "message":  "Battery is fully charged. You may unplug your charger.",
                "icon":     "battery-level-100-charged-symbolic",
            }
        # }}}

        # {{{ Charging
        case "Charging":
            batPercentage      = int(bat.Percentage)
            roundBatPercentage = round(batPercentage, -1)
            chargingIcon       = f"battery-level-{roundBatPercentage}-charging-symbolic"

            notiMsg["Charging"] = {
                "appName":  "Battery",
                "title":    "Charging",
                "message":  "Charger plugged in.",
                "icon":     chargingIcon,
            }
        # }}}

        # {{{ Discharging
        case "Discharging":
            batPercentage      = int(bat.Percentage)
            roundBatPercentage = round(batPercentage, -1)
            dischargingIcon    = f"battery-level-{roundBatPercentage}-symbolic"

            notiMsg["Discharging"] = {
                "appName":  "Battery",
                "title":    "Discharging",
                "message":  "Charger unplugged.",
                "icon":     dischargingIcon,
            }
        # }}}

        # {{{ Low
        case "Low":
            batPercentage = int(bat.Percentage)
            timeToEmpty   = convertSeconds(bat.TimeToEmpty)

            if timeToEmpty != "0 h 0 min":
                lowMsg   = f"Battery is at {batPercentage}%. Please plug in a charger.\n{timeToEmpty} remaining."
            else: lowMsg = f"Battery is at {batPercentage}%. Please plug in a charger."

            notiMsg["Low"] = {
                "appName":  "Battery",
                "title":    "Low battery",
                "message":  lowMsg,
                "duration": 0,
                "icon":     "battery-caution-symbolic",
            }
        # }}}

        # {{{ Critical
        case "Critical":
            batPercentage = int(bat.Percentage)
            timeToEmpty   = convertSeconds(bat.TimeToEmpty)

            if timeToEmpty != "0 h 0 min":
                criticalMsg   = f"Battery is at {batPercentage}%. Plug in a charger immediately or save your work and shut down.\n{timeToEmpty} remaining."
            else: criticalMsg = f"Battery is at {batPercentage}%. Plug in a charger immediately or save your work and shut down."

            notiMsg["Critical"] = {
                "appName":  "Battery",
                "title":    "Critically low battery",
                "message":  criticalMsg,
                "duration": 0,
                "icon":     "battery-empty-symbolic",
            }
        # }}}
# }}}

# {{{ Send refreshed notification
def notifyRefreshed(which):
    refreshNotif(which)
    notify(**notiMsg[which])
# }}}

# {{{ Handle property changes
def handlePropChanges(interface, changedProperties, invalidatedProperties):
    global lastState

    if "State" in changedProperties != lastState:
        match changedProperties["State"]:
            case 1: notifyRefreshed("Charging")
            case 2: notifyRefreshed("Discharging")
            case 4: notifyRefreshed("Charged")

    if "WarningLevel" in changedProperties:
        match changedProperties["WarningLevel"]:
            case 3: notifyRefreshed("Low")
            case 4: notifyRefreshed("Critical")
# }}}
# }}}

# {{{ Defining the main elements
bat  = sysBus.get(upowerBusName, batteryPath)
loop = GLib.MainLoop()

# {{{ Notification function
def notify(appName="Battery", title="No title", message="No message body", duration=-1, icon="battery-level-100-symbolic"):
    bus      = pydbus.SessionBus()
    notifs   = bus.get(".Notifications")
    duration *= 1000

    notifs.Notify(appName, 0, icon, title, message, [], {}, duration)
# }}}
# }}}

try:
    # {{{ Main
    bat.PropertiesChanged.connect(handlePropChanges)
    loop.run()
    # }}}
except KeyboardInterrupt:
    # {{{ Gracefully exit
    loop.quit()
    exit(0)
    # }}}
