# Connect to WiFi
import network
import env
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(env.WLAN_SSID, env.WLAN_PASSWORD)

# WebREPL (8266)
import webrepl
webrepl.start()

import time
pprefix = 'BOOT:'
print()
print(pprefix, 'WiFi connection success')
time.sleep(1)
print(pprefix, "IP:", wlan.ifconfig()[0])
print()

import gc
gc.collect()
