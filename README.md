# OnlyFans

**OnlyFans** is a Python utility for managing fan speeds on HP OMEN laptops, enabling users to manually adjust fan speeds, configure temperature-based speed curves, and manage fan boost settings. It also offers an automated service mode for temperature-dependent fan control.

## Features

-   **Manual Fan Speed Control:** Set specific RPM values for each fan.
-   **Temperature Curves:** Customize fan speeds based on temperature thresholds.
-   **Boost Mode:** Toggle maximum fan speed for intensive cooling.
-   **Automated Service:** Optionally control fans based on real-time temperature readings.

---

## Prerequisites

-   Python 3.x
-   Python libraries: `click`, `tomlkit`, `click_aliases`

Install the required libraries with pip:

```sh
sudo pip install click tomlkit click-aliases
```

> [!IMPORTANT]
> Ensure Secure Boot is disabled in your BIOS to enable communication with the laptop's Embedded Controller (EC) module.

---

## Supported Devices

-   This utility is optimized for HP OMEN laptops with dual fans.
-   **Unsupported Models:** HP Victus and possibly other non-OMEN models.

---

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ifsvivek/onlyfans.git
    cd onlyfans
    ```

2. **Update the Script Path in `fans.sh`:**

    Open `fans.sh` and set the path to `omen-fan.py`. For instance, if `omen-fan.py` is in `~/Documents/omen`, your `fans.sh` should look like:

    ```sh
    #!/bin/bash
    exec gnome-terminal -- bash -c "
      cd ~/Documents/omen && \
      sudo bash -c 'python3 omen-fan.py e start'
    "
    ```

3. **Make `fans.sh` Executable:**

    ```sh
    chmod +x fans.sh
    ```

---

## Usage

### Starting the Service

To begin automatic fan control:

```sh
./fans.sh
```

This command opens a terminal window to start `omen-fan.py` with necessary permissions.

---

### Command-Line Interface (CLI)

The utility offers a flexible CLI to manage fan settings. Below are available commands:

#### `bios-control`

Enable or disable BIOS-based fan control.

```sh
sudo python3 omen-fan.py bios-control [True|False]
```

-   `True` - BIOS controls the fans.
-   `False` - Manual control via this script.

#### `boost`

Toggle fan boost mode for maximum fan speed.

```sh
sudo python3 omen-fan.py boost [True|False]
```

-   `True` - Enables maximum speed.
-   `False` - Returns to normal fan speeds.

#### `configure`

Configure fan speed behavior based on temperature thresholds.

```sh
sudo python3 omen-fan.py configure --temp-curve "50,60,70,75,80,90" --speed-curve "50,60,80,100,100,100" --idle-speed 25 --poll-interval 1
```

Options:

-   `--temp-curve`: List of temperature thresholds (°C).
-   `--speed-curve`: Fan speeds for each temperature threshold.
-   `--idle-speed`: Speed below the lowest threshold.
-   `--poll-interval`: How often (in seconds) the temperature is checked.

> [!TIP]
> Ensure `temp-curve` and `speed-curve` lists have equal values, with temperature values in ascending order.

To view current configuration:

```sh
sudo python3 omen-fan.py configure --view
```

#### `service`

Start or stop the fan control service.

```sh
sudo python3 omen-fan.py service [start|stop]
```

-   `start`: Launches fan control.
-   `stop`: Ends fan control.

#### `info`

Display current fan and service status.

```sh
sudo python3 omen-fan.py info
```

Outputs:

-   Service status
-   BIOS control status
-   Fan speeds
-   Boost mode status

#### `set`

Manually assign RPM values to each fan.

```sh
sudo python3 omen-fan.py set [fan1_speed] [fan2_speed]
```

-   `fan1_speed`: Speed for fan 1 (RPM).
-   `fan2_speed`: Speed for fan 2 (RPM).

> [!TIP]
> RPM values should be within the hardware’s capabilities (e.g., 30 = 3000 RPM).

**Example:**

Set both fans to 3000 RPM:

```sh
sudo python3 omen-fan.py set 30
```

Set fan 1 to 3000 RPM and fan 2 to 4000 RPM:

```sh
sudo python3 omen-fan.py set 30 40
```

#### `version`

View the utility version.

```sh
python3 omen-fan.py version
```

---

## Configuration

A `config.toml` file will be generated on first run, storing custom temperature and speed curves, idle speed, and polling intervals.

---

## License

Licensed under the MIT License. See [LICENSE](./LICENSE) for more details.

---

## Disclaimer

This utility is built specifically for HP OMEN laptops. Usage on unsupported models may result in unintended behavior. The authors are not liable for damages from using this tool.
