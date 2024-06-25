## Turn your ESP32 into a Wake on Lan device

This project uses [MicroPython](https://micropython.org/) as a base.

Works with a Telegram bot, connects to local wifi network.

You have to rename `env.example.py` to `env.py` and fill in the environment variables.

## Step 1

Follow the [MicroPython installer guide](https://micropython.org/download/ESP32_GENERIC/) to get started.

Have at least [Python](https://www.python.org/downloads/) 3.7 installed

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
