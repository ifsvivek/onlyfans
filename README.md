# OnlyFans

OnlyFans is an application designed to manage the fan settings on Omen laptops. It utilizes PyQt5 for the graphical user interface and various system libraries for hardware interaction.

## Table of Contents

- [OnlyFans](#onlyfans)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [File Structure](#file-structure)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

1. **Download the latest release** from the [releases page](https://github.com/ifsvivek/onlyfans/releases).
2. Open a terminal and navigate to the directory where the file was downloaded.
3. Run the following command to install the package:
    ```sh
    sudo dpkg -i OnlyFans.deb
    ```
4. Launch the application with:
    ```sh
    sudo onlyfans
    ```

## Usage

The application is designed to be simple and intuitive. The main window displays the current fan speed and the temperature of the CPU and GPU. You can adjust the fan speed using the slider at the bottom of the window. The application will automatically adjust the fan speed based on the temperatures of the CPU and GPU.

> **Note:**  
> The application requires root privileges to access hardware sensors and control the fans. Ensure you run the application with `sudo` or as the root user.  
> The application is specifically designed for Omen laptops.  
> Please note that the application is still in development and may not function correctly on all systems.

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
│       ├── bin/
│       │   ├── onlyfans
│       │   └── install.sh
│       ├── lib/
│       │   └── onlyfans/
│       │       └── deps/
│       │           └── service.py
├── README.md
├── fan_control.py
├── main.py
├── main.spec
└── .gitignore
```

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request. For any questions or issues, open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.