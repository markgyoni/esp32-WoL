# WebREPL (8266)
import webrepl
webrepl.start()

# Connect to WiFi
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Tbone  WiFi', 'paradicsom2022')