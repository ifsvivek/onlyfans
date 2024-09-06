# OnlyFans

OnlyFans is an application designed to control the fan settings on Omen Laptops. It utilizes PyQt5 for the graphical user interface and various system libraries for hardware interaction.

## Table of Contents

- Installation
- Usage
- [File Structure](#file-structure)
- Contributing
- License

## Installation

1. **Download the latest release from the [releases page](https://github.com/ifsvivek/onlyfans/releases)
2. open a terminal and navigate to the directory where the file was downloaded.
3. Run the following command to install the package:
    ```sh
    sudo dpkg -i OnlyFans.deb
    ```
4. Run the following command to launch the application:
    ```sh
    sudo onlyfans
    ```

## Usage

The application is designed to be simple and easy to use. The main window displays the current fan speed and temperature of the CPU and GPU. The user can adjust the fan speed using the slider at the bottom of the window. The application will automatically adjust the fan speed based on the temperature of the CPU and GPU.

> [!note]
> The application requires root privileges to access the hardware sensors and control the fans. Make sure to run the application with `sudo` or as the root user.  
> The application is designed to work with Omen Laptops.  
> The application is still in development and may not work correctly on all systems.


## File Structure

```
onlyfans/
├── build/
│   ├── main/
├── env/
├── OnlyFans/
│   ├── DEBIAN/
│   │   └── control
│   └── usr/
│   │   ├── bin/
│   │   │   └── onlyfans
│   │   │   └── install.sh
│   │   ├── lib/
│   │   │   └── onlyfans/
│   │   │       └── deps/
|   |   |       └── service.py
├── README.md
├── fan_control.py
├── main.py
├── main.spec
└── .gitignore
```

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**
    ```sh
    git checkout -b feature-branch
    ```
3. **Make your changes and commit them:**
    ```sh
    git commit -m 'Add some feature'
    ```
4. **Push to the branch:**
    ```sh
    git push origin feature-branch
    ```
5. **Create a pull request.**

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Package Details

- **Package:** OnlyFans
- **Version:** 1.0
- **Section:** base
- **Priority:** optional
- **Architecture:** all
- **Depends:** python3, python3-pyqt5
- **Maintainer:** github.com/ifsvivek
- **Description:** App for controlling Fans on Omen Laptop