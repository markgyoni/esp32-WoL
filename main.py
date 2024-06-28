import env
import network
import machine  # type: ignore
import time
import socket
import binascii
import requests  # type: ignore


# def microdot_start():
#     from microdot import Microdot

#     app = Microdot()

#     @app.route("/")
#     async def index(request):
#         return "Hello, world!"

#     app.run(port=80)


# microdot_start()


# Connect to WiFi if not yet connected
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(env.WLAN_SSID, env.WLAN_PASSWORD)
    else:
        pass


def send_wol_packet(mac_address, broadcast_ip="255.255.255.255", port=9):
    magic_packet = b"\xff" * 6 + (binascii.unhexlify(mac_address.replace(":", "")) * 16)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(magic_packet, (broadcast_ip, port))
    s.close()


target_mac_address = env.MAC_ADDRESS

offset = 0
authorized = env.AUTHORIZED_USERS

failure_count = 0

wifi_connect()

while True:
    time.sleep(5)

    body = {}

    try:
        body = requests.get(
            f"https://api.telegram.org/{env.TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset + 1}"
        ).json()
    except:
        print("Unable to fetch updates")
        continue

    updates = body["result"]

    for update in updates:
        offset = update["update_id"]

        if (
            update["message"]["from"]["id"] in authorized
            and update["message"]["text"] == "/wol"
        ):
            try:
                send_wol_packet(target_mac_address)

                requests.get(
                    f'https://api.telegram.org/{env.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={update["message"]["from"]["id"]}&text=Sent%20WoL%20packet.'
                )
            except:
                print("Unable to send WoL or message.")

    if failure_count >= 5:
        machine.reset()
