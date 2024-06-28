## Turn your ESP32 into a Wake on Lan device

This project uses [MicroPython](https://micropython.org/) as a base.

Works with a Telegram bot, connects to local wifi network.

You have to rename `env.example.py` to `env.py` and fill in the environment variables.

I recommend using Linux for the flash and setup of the device. After that, you can use the webREPL site on port 8266 to control the ESP32.

## Step 1

Follow the [MicroPython installer guide](https://micropython.org/download/ESP32_GENERIC/) to get started.

Have at least [Python](https://www.python.org/downloads/) 3.7 installed

You should run everything here as root.

- You will need to install the [esptool.py](https://github.com/espressif/esptool) tool to flash the firmware.

  ```
  pip install esptool
  ```

- Erase the ESP32 flash memory

  ```
  esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
  ```

- Flash the new firmware

  ```
  esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-date-version.bin
  ```

- Connect with serial

  - Find the connected device

    ```
    mesg | grep tty
    ```

  - If you see it connecting and disconnecting immidiately after, try uninstalling this package: (It solved it for me) `apt-get autoremove brltty`
  - Install minicom or use any other package

    ```
    apt-get install minicom
    ```

  - Connect to the device

    ```
    minicom -b 115200 -o -D /dev/ttyUSB0
    ```

- Connect to the WiFi network

  https://docs.micropython.org/en/latest/esp32/quickref.html#wlan

- Enable WebREPL (port 8266)

  https://docs.micropython.org/en/latest/esp32/quickref.html#webrepl-web-browser-interactive-prompt
