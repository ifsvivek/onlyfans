import sys
import subprocess
import signal
import os
import glob
from time import sleep
from PyQt5 import QtWidgets
import tomlkit

# Backend constants
ECIO_FILE = "/sys/kernel/debug/ec/ec0/io"
IPC_FILE = "/tmp/omen-fand.PID"
DEVICE_FILE = "/sys/devices/virtual/dmi/id/product_name"
CONFIG_FILE = "/etc/omen-fan/config.toml"

# Backend variables
BOOST_FILE = next(
    iter(glob.glob("/sys/devices/platform/hp-wmi/hwmon/*/pwm1_enable")), None
)
FAN1_SPEED_FILE = next(
    iter(glob.glob("/sys/devices/platform/hp-wmi/hwmon/*/fan1_input")), None
)
FAN2_SPEED_FILE = next(
    iter(glob.glob("/sys/devices/platform/hp-wmi/hwmon/*/fan2_input")), None
)

FAN1_OFFSET = 52
FAN2_OFFSET = 53
BIOS_OFFSET = 98
TIMER_OFFSET = 99
FAN1_MAX = 59
FAN2_MAX = 59
DEVICE_LIST = ["OMEN by HP Laptop 16"]


def is_root():
    if os.geteuid() != 0:
        print("  Root access is required.")
        sys.exit(1)
    return True


def startup_check():
    if not os.path.isfile(CONFIG_FILE):
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Created by omen-fan script"))
        doc.add("service", tomlkit.table())
        doc["service"]["TEMP_CURVE"] = [50, 60, 70, 75, 80, 90]
        doc["service"]["SPEED_CURVE"] = [50, 60, 80, 100, 100, 100]
        doc["service"]["IDLE_SPEED"] = 0
        doc["service"]["POLL_INTERVAL"] = 1
        doc.add("script", tomlkit.table())
        doc["script"]["BYPASS_DEVICE_CHECK"] = 0
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as file:
            file.write(tomlkit.dumps(doc))
        print("  INFO: Configuration file has been created")
    else:
        with open(CONFIG_FILE, "r") as file:
            doc = tomlkit.loads(file.read())
        device_name = open(DEVICE_FILE).read()
        if (
            any(device not in device_name for device in DEVICE_LIST)
            and doc["script"]["BYPASS_DEVICE_CHECK"] != 1
        ):
            print("  ERROR: Device not supported.")
            sys.exit(1)


def load_ec_module():
    if "ec_sys" not in str(subprocess.check_output("lsmod")):
        subprocess.run(["modprobe", "ec_sys", "write_support=1"], check=True)
    if not os.stat(ECIO_FILE).st_mode & 0o200:
        subprocess.run(["modprobe", "-r", "ec_sys"], check=True)
        subprocess.run(["modprobe", "ec_sys", "write_support=1"], check=True)


def update_fan(speed1, speed2):
    bios_control(False)
    with open(ECIO_FILE, "r+b") as ec:
        ec.seek(FAN1_OFFSET)
        ec.write(bytes([int(speed1)]))
        ec.seek(FAN2_OFFSET)
        ec.write(bytes([int(speed2)]))


def bios_control(enabled):
    with open(ECIO_FILE, "r+b") as ec:
        ec.seek(BIOS_OFFSET)
        ec.write(bytes([6 if not enabled else 0]))
        sleep(0.1)
        if not enabled:
            ec.seek(TIMER_OFFSET)
            ec.write(bytes([0]))


def parse_rpm(rpm, fan, max_speed):
    is_percent = "%" in rpm
    rpm = rpm.replace("%", "")
    try:
        rpm = int(rpm)
    except ValueError:
        print(f"  ERROR: '{rpm}' is not a valid integer.")
        sys.exit(1)
    if is_percent:
        return int(max_speed * rpm / 100)
    elif 0 <= rpm <= max_speed:
        return rpm
    else:
        print(
            f"  ERROR: '{rpm}' is not a valid RPM/100 value for Fan{fan}. Min: 0 Max: {max_speed}"
        )
        sys.exit(1)


def configure(temp_curve=None, speed_curve=None, idle_speed=None, poll_interval=None):
    is_root()
    with open(CONFIG_FILE, "r") as file:
        doc = tomlkit.loads(file.read())
    temp_curve = [
        int(x) for x in (temp_curve or doc["service"]["TEMP_CURVE"]).split(",")
    ]
    speed_curve = [
        int(x) for x in (speed_curve or doc["service"]["SPEED_CURVE"]).split(",")
    ]
    if len(temp_curve) != len(speed_curve):
        raise ValueError("TEMP_CURVE and SPEED_CURVE must have the same length")
    if not all(temp_curve[i] <= temp_curve[i + 1] for i in range(len(temp_curve) - 1)):
        raise ValueError("TEMP_CURVE must be in ascending order")
    if idle_speed is not None:
        doc["service"]["IDLE_SPEED"] = idle_speed
    if poll_interval is not None:
        doc["service"]["POLL_INTERVAL"] = poll_interval
    with open(CONFIG_FILE, "w") as file:
        file.write(tomlkit.dumps(doc))


def service(arg):
    is_root()
    load_ec_module()
    if arg in ["start", "1"]:
        if os.path.isfile(IPC_FILE):
            with open(IPC_FILE, "r") as ipc:
                print(f"  omen-fan service is already running with PID:{ipc.read()}")
        else:
            subprocess.Popen(["python3", "/usr/local/lib/onlyfans/service.py"])
            print("  omen-fan service has been started")
    elif arg in ["stop", "0"]:
        if os.path.isfile(IPC_FILE):
            with open(IPC_FILE, "r") as ipc:
                try:
                    os.kill(int(ipc.read()), signal.SIGTERM)
                except ProcessLookupError:
                    print("  omen-fan service was killed unexpectedly.")
                    os.remove(IPC_FILE)
                    sys.exit(1)
            print("  omen-fan service has been stopped")
            bios_control(True)
        else:
            print("  omen-fan service is not running")


def info():
    result = {}
    if os.path.isfile(IPC_FILE):
        with open(IPC_FILE, "r") as ipc:
            result["Status"] = "Running"
            result["PID"] = ipc.read().strip()
            result["BIOS Control"] = "Disabled"
    else:
        result["Status"] = "Stopped"
        if is_root():
            load_ec_module()
            with open(ECIO_FILE, "rb") as ec:
                ec.seek(BIOS_OFFSET)
                result["BIOS Control"] = (
                    "Disabled" if int.from_bytes(ec.read(1), "big") == 6 else "Enabled"
                )

    if FAN1_SPEED_FILE:
        with open(FAN1_SPEED_FILE, "r") as fan1:
            result["Fan 1"] = f"{fan1.read().strip()} RPM"
    else:
        result["Fan 1"] = "Not available"

    if FAN2_SPEED_FILE:
        with open(FAN2_SPEED_FILE, "r") as fan2:
            result["Fan 2"] = f"{fan2.read().strip()} RPM"
    else:
        result["Fan 2"] = "Not available"

    if BOOST_FILE:
        with open(BOOST_FILE, "r") as boost:
            result["Fan Boost"] = (
                "Enabled" if boost.read().strip() == "0" else "Not available"
            )
    else:
        result["Fan Boost"] = "Not available"

    return result


def set_fan_speed(speed1, speed2=None):
    is_root()
    load_ec_module()
    if os.path.isfile(IPC_FILE):
        print("  WARNING: omen-fan service running, may override fan speed")
    if speed2 is None:
        update_fan(parse_rpm(speed1, 1, FAN1_MAX), parse_rpm(speed1, 2, FAN2_MAX))
    else:
        update_fan(parse_rpm(speed1, 1, FAN1_MAX), parse_rpm(speed2, 2, FAN2_MAX))


class FanControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Fan Control")
        self.setGeometry(100, 100, 400, 300)

        self.startButton = QtWidgets.QPushButton("Start Service", self)
        self.startButton.setGeometry(50, 50, 150, 30)
        self.startButton.clicked.connect(self.start_service)

        self.stopButton = QtWidgets.QPushButton("Stop Service", self)
        self.stopButton.setGeometry(200, 50, 150, 30)
        self.stopButton.clicked.connect(self.stop_service)

        self.setFanSpeedButton = QtWidgets.QPushButton("Set Fan Speed", self)
        self.setFanSpeedButton.setGeometry(50, 200, 150, 30)
        self.setFanSpeedButton.clicked.connect(self.set_fan_speed)

        self.fanSpeedInput = QtWidgets.QLineEdit(self)
        self.fanSpeedInput.setGeometry(200, 200, 100, 30)
        self.fanSpeedInput.setPlaceholderText("Speed (0-100%)")

        self.pidLabel = QtWidgets.QLabel("PID:", self)
        self.pidLabel.setGeometry(50, 250, 100, 30)
        self.pidValue = QtWidgets.QLabel("N/A", self)
        self.pidValue.setGeometry(150, 250, 100, 30)

        self.updateFanInfo()

    def start_service(self):
        if is_root():
            service("start")
            self.updateFanInfo()

    def stop_service(self):
        if is_root():
            service("stop")
            self.updateFanInfo()

    def set_fan_speed(self):
        if is_root():
            speed = self.fanSpeedInput.text()
            if speed:
                set_fan_speed(speed)
                self.updateFanInfo()

    def updateFanInfo(self):
        if is_root():
            status_info = info()
            self.pidValue.setText(status_info.get("PID", "N/A"))


if __name__ == "__main__":
    # code to run ask for root access if not already
    
    app = QtWidgets.QApplication(sys.argv)
    window = FanControlWindow()
    window.show()
    sys.exit(app.exec_())
