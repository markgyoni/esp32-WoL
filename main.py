import socket
import binascii
import network
import env

pprefix = "MAIN:"

def wifi_connect():   
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(env.WLAN_SSID, env.WLAN_PASSWORD)
        print(pprefix, 'WiFi connection success')
        print(pprefix, "IP:", wlan.ifconfig())
    else:
        pass

def send_wol_packet(mac_address, broadcast_ip='255.255.255.255', port=9):
    magic_packet = b'\xff' * 6 + (binascii.unhexlify(mac_address.replace(':', '')) * 16)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(magic_packet, (broadcast_ip, port))
    s.close()

target_mac_address = env.MAC_ADDRESS

offset = 0
authorized = env.AUTHORIZED_USERS

failure_count = 0

wifi_connect()

# WEBSITE

try:
  import usocket as socket # type: ignore
except:
  import socket

from machine import Pin # type: ignore
led = Pin(2, Pin.OUT)

def web_page():

  import uping
  pingResult = uping.ping('192.168.1.250', count=2)
  pcstatus = ""
  if pingResult[1] == 0:
      print("PC offline")
      pcstatus = "Off"
  else:
      print("PC online")
      pcstatus = "On"
  
  html = """<html>
   <head>
      <title>ESP32-WoL</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="icon" href="data:,">
      <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
         h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
         border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
         .button2{background-color: #4286f4;}
      </style>
   </head>
   <body>
      <h1>Computer status</h1>
      <p>State: <strong>""" + pcstatus + """</strong></p>
      <p><a href="/?led=on"><button class="button">ON</button></a></p>
      <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
      <script>
        function toggleLED() {
          fetch('/toggle')
            .then(response => response.json())
            .then(data => {
              if (data.led_state === 1) {
                document.getElementById('led-status').innerText = 'On';
              } else {
                document.getElementById('led-status').innerText = 'Off';
              }
            });
        }
      </script>
      <p>LED Status: <strong id="led-status">""" + ('On' if led.value() == 1 else 'Off') + """</strong></p>
      <p><button class="button" onclick="toggleLED()">Toggle LED</button></p>
   </body>
</html>"""

  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()