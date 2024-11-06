#!/usr/bin/env python3

import os
import signal
import sys
from time import sleep
import tomlkit
from bisect import bisect_left

ECIO_FILE = "/sys/kernel/debug/ec/ec0/io"
IPC_FILE = "/tmp/omen-fand.PID"
CONFIG_FILE = "/etc/omen-fan/config.toml"

FAN1_OFFSET = 52  # 0x34
FAN2_OFFSET = 53  # 0x35
BIOS_OFFSET = 98  # 0x62
TIMER_OFFSET = 99  # 0x63
CPU_TEMP_OFFSET = 87  # 0x57
GPU_TEMP_OFFSET = 183  # 0xB7

FAN1_MAX = 59
FAN2_MAX = 59

with open(CONFIG_FILE, "r") as file:
    doc = tomlkit.loads(file.read())
    TEMP_CURVE = doc["service"]["TEMP_CURVE"].unwrap()
    SPEED_CURVE = doc["service"]["SPEED_CURVE"].unwrap()
    IDLE_SPEED = doc["service"]["IDLE_SPEED"].unwrap()
    POLL_INTERVAL = doc["service"]["POLL_INTERVAL"].unwrap()

# Precalculate slopes to reduce compute time.
slope = []
for i in range(1, len(TEMP_CURVE)):
    speed_diff = SPEED_CURVE[i] - SPEED_CURVE[i - 1]
    temp_diff = TEMP_CURVE[i] - TEMP_CURVE[i - 1]
    slope_val = round(speed_diff / temp_diff, 2)
    slope.append(slope_val)


def is_root():
    if os.geteuid() != 0:
        print("  Root access is required for this service.")
        print("  Please run this service as root.")
        sys.exit(1)


def sig_handler(signum, frame):
    os.remove("/tmp/omen-fand.PID")
    bios_control(True)
    sys.exit()


def update_fan(speed1, speed2):
    with open(ECIO_FILE, "r+b") as ec:
        ec.seek(FAN1_OFFSET)
        ec.write(bytes([int(speed1)]))
        ec.seek(FAN2_OFFSET)
        ec.write(bytes([int(speed2)]))


def get_temp():
    with open(ECIO_FILE, "rb") as ec:
        ec.seek(CPU_TEMP_OFFSET)
        temp_c = int.from_bytes(ec.read(1), "big")
        ec.seek(GPU_TEMP_OFFSET)
        temp_g = int.from_bytes(ec.read(1), "big")
    return max(temp_c, temp_g)


def bios_control(enabled):
    if enabled is False:
        with open(ECIO_FILE, "r+b") as ec:
            ec.seek(BIOS_OFFSET)
            ec.write(bytes([6]))
            sleep(0.1)
            ec.seek(TIMER_OFFSET)
            ec.write(bytes([0]))
    elif enabled is True:
        with open(ECIO_FILE, "r+b") as ec:
            ec.seek(BIOS_OFFSET)
            ec.write(bytes([0]))
            ec.seek(FAN1_OFFSET)
            ec.write(bytes([0]))
            ec.seek(FAN2_OFFSET)
            ec.write(bytes([0]))


signal.signal(signal.SIGTERM, sig_handler)

with open(IPC_FILE, "w", encoding="utf-8") as ipc:
    ipc.write(str(os.getpid()))

speed_old = -1
is_root()

while True:
    temp = get_temp()

    if temp <= TEMP_CURVE[0]:
        speed = IDLE_SPEED
    elif temp >= TEMP_CURVE[-1]:
        speed = SPEED_CURVE[-1]
    else:
        i = bisect_left(TEMP_CURVE, temp)
        y0 = SPEED_CURVE[i - 1]
        x0 = TEMP_CURVE[i - 1]

        speed = y0 + slope[i - 1] * (temp - x0)

    if speed_old != speed:
        speed_old = speed
        update_fan(FAN1_MAX * speed / 100, FAN2_MAX * speed / 100)

    bios_control(False)
    sleep(POLL_INTERVAL)
