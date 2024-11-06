# OnlyFans

OnlyFans is a Python-based utility for controlling the fan speeds on HP OMEN laptops. It allows you to manually set fan speeds, configure temperature and speed curves, and manage fan boost settings. The utility also includes a service mode for automatic fan control based on temperature readings.

## Prerequisites

-   Python 3.x
-   `click` library
-   `tomlkit` library
-   `click_aliases` library

You can install the required libraries using pip:

```sh
sudo pip install click tomlkit click-aliases
```

> [!Important]
> Secure Boot must be disabled in the BIOS settings to allow the utility to access the Embedded Controller (EC) module.

## Supported Models

-   The utility is designed for HP OMEN laptops with dual fans. I haven't tested it on other models, so it may not work as expected.
-   HP Victus laptops are not supported at the moment.

## Installation

1. Clone the repository to your local machine:

```sh
git clone https://github.com/ifsvivek/onlyfans.git
cd onlyfans
```

2. Make the scripts executable:

> [!Important]
> Make sure to change the address of the script in the `fans.sh` file to the correct path where `omen-fan.py` is located.

Open the `fans.sh` file in a text editor and update the path to the `omen-fan.py` script. For example, if the script is located in `~/Documents/omen`, the `fans.sh` file should look like this:

```sh
#!/bin/bash

exec gnome-terminal -- bash -c "
  cd ~/Documents/omen && \
  sudo bash -c 'python3 omen-fan.py e start'
"
```

After updating the path, make the `fans.sh` script executable by running the following command:

```sh
chmod +x fans.sh
```

This command changes the permissions of the `fans.sh` file to make it executable, allowing you to run it as a script.

## Usage

### Starting the Service

To start the fan control service, run the following command:

```sh
./fans.sh
```

This will open a new terminal window and start the `omen-fan.py` service with root privileges.

### Command Line Interface

The `omen-fan.py` script provides several commands for managing fan settings. Below are the available commands:

#### `bios-control`

Enable or disable BIOS control of the fans.

```sh
sudo python3 omen-fan.py bios-control [True|False]
```

-   `True`: Enables BIOS control of the fans.
-   `False`: Disables BIOS control of the fans, allowing manual control.

This command ensures that the script has root privileges and loads the necessary EC (Embedded Controller) module before enabling or disabling BIOS control.

#### `boost`

Enable or disable fan boost mode.

```sh
sudo python3 omen-fan.py boost [True|False]
```

-   `True`: Enables fan boost mode, setting the fans to maximum speed.
-   `False`: Disables fan boost mode, allowing normal operation.

This command checks for the presence of the boost file and writes the appropriate value to enable or disable boost mode.

#### `configure`

Configure temperature and speed curves, idle speed, and polling interval.

```sh
sudo python3 omen-fan.py configure --temp-curve "50,60,70,75,80,90" --speed-curve "50,60,80,100,100,100" --idle-speed 25 --poll-interval 1
```

-   `--temp-curve`: A comma-separated list of temperature thresholds.
-   `--speed-curve`: A comma-separated list of fan speeds corresponding to the temperature thresholds.
-   `--idle-speed`: The fan speed when the temperature is below the first threshold.
-   `--poll-interval`: The interval (in seconds) at which the script checks the temperature.

> [!Important]
> The temperature and speed curves should have the same number of values, and the temperature curve should be in ascending order. The idle speed should be a value between 0% and 100%, and the polling interval should be a positive integer.

To view the current configuration:

```sh
sudo python3 omen-fan.py configure --view
```

This command reads the configuration file, updates the specified settings, and writes the changes back to the file. It also validates that the temperature and speed curves have the same length and that the temperature curve is in ascending order.

#### `service`

Start or stop the fan control service.

```sh
sudo python3 omen-fan.py service [start|stop]
```

-   `start`: Starts the fan control service.
-   `stop`: Stops the fan control service.

This command checks if the service is already running and starts or stops it accordingly. It also updates the BIOS control state and manages the PID file for the service.

#### `info`

Display the current status of the fans and the service.

```sh
sudo python3 omen-fan.py info
```

This command displays the following information:

-   Service status (running or stopped)
-   BIOS control status (enabled or disabled)
-   Current fan speeds
-   Fan boost status (enabled or disabled)

It reads the necessary files to gather this information and prints it to the console.

#### `set`

Manually set the fan speeds.

```sh
sudo python3 omen-fan.py set [fan1_speed] [fan2_speed]
```

-   `fan1_speed`: The speed for fan 1 (RPM value).
-   `fan2_speed`: The speed for fan 2 (RPM value).

> [!Important]
> RPM values should be between 0 and your fan's maximum speed.
> To calculate the maximum speed of your fan:
>
> -   59 corresponds to 5900 RPM
> -   40 corresponds to 4000 RPM

If only one speed is provided, both fans will be set to the same speed. This command parses the provided speeds, validates them, and updates the fan speeds accordingly.

**Example Usage:**

1. Set both fans to 3000 RPM:

```sh
sudo python3 omen-fan.py set 30
```

In this example, `30` represents 3000 RPM for both fans.

2. Set fan 1 to 3000 RPM and fan 2 to 4000 RPM:

```sh
sudo python3 omen-fan.py set 30 40
```

In this example, `30` represents 3000 RPM for fan 1, and `40` represents 4000 RPM for fan 2.

#### `version`

Display the version of the utility.

```sh
python3 omen-fan.py version
```

This command simply prints the version information of the utility.

## Configuration

The configuration file is located at `config.toml`. It is automatically created during the first run of the script if it does not exist. The configuration file includes settings for temperature and speed curves, idle speed, and polling interval.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Disclaimer

This utility is designed for HP OMEN laptops and may not work on other models. Use at your own risk. The authors are not responsible for any damage caused by using this utility.
