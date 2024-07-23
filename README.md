# CAN Log Parser
![Build Status](https://github.com/kiranj26/CAN-Log-Parser/actions/workflows/ci.yml/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4a476526a37145f2922f58a6f903ff27)](https://app.codacy.com/gh/kiranj26/CAN-Log-Parser/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![Flake8 Linting](https://img.shields.io/badge/flake8-linting-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/github/license/kiranj26/CAN-Log-Parser)    
This repository contains a Python-based tool to parse DBC formatted CAN log files and plot the signals. It leverages `cantools` for parsing DBC files and `matplotlib` for plotting signals, providing an easy way to visualize CAN signal data.

## Features

- Parse DBC files to extract signal definitions
- Read and parse CAN log files
- Decode signals from CAN messages
- Plot the decoded signals

## Requirements

All required packages are listed in the `requirements.txt` file.

- Python 3.6 or higher
- cantools
- matplotlib

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kiranj26/CAN-Log-Parser.git
    cd CAN-Log-Parser
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your DBC file and log file in the `data/` directory.

2. Run the main script with the appropriate arguments:

    ```bash
    python src/main.py test SAF_SpeedTest
    ```

    or

    ```bash
    python src/main.py test SAF_SpeedTest 43.2 45.6
    ```

## Repository Structure

- `src/`: Contains the main script and related files.
  - `main.py`: Main script to run the tool.
- `data/`: Directory to place your DBC and log files.
- `requirements.txt`: List of dependencies.

## Script Description

### parse_dbc(file_path)

Parses the DBC file located at `file_path`.

### parse_log(db, log_file_path)

Parses the log file located at `log_file_path` using the parsed DBC data.

### process_message(db, message_lines, parsed_data)

Processes a single CAN message and extracts the signals.

### print_parsed_data(parsed_data)

Prints the parsed CAN data.

### plot_signals(parsed_data, signal_name, start_time, end_time)

Plots the specified CAN signal within the given time range.

## Example

To run the script, navigate to the directory containing `main.py` and execute the following commands:

```bash
python src/main.py test SAF_SpeedTest
OR
python src/main.py test SAF_SpeedTest 43.2 45.6
```

These commands will parse the test.dbc and test_log.txt files located in the data/ directory, process the CAN messages, and generate a plot for the SAF_SpeedTest signal.

## Output Screenshots

<div align="center">
  <img src="https://github.com/user-attachments/assets/ae5de356-ce91-4c4b-9cac-8f3f02ae049d" width="600" height="400" />
  <img src="https://github.com/user-attachments/assets/d0fe7b06-18b1-4ff4-be53-82c877288097" width="600" height="400" />
</div>


## GUI Features
### Overview

The GUI built using PyQt5 allows users to interactively select and plot CAN signals from the log file.

### Features

- **Multiple Plot Options**: Select which subplot to plot the signals in, allowing for easy comparison of multiple signals.
- **Data Filtering**: Filter the data to be plotted by selecting specific start and end times.
- **Advanced Plot Customization**: Customize the plot's appearance, including zooming, panning, and adjusting plot sizes.
- **Data Export and Import**: Export the plotted data to CSV or import previously saved data for further analysis.
- **Interactive Features**: Zoom, pan, and interact with the plot to analyze specific sections of the data.
- **Annotations and Markers**: Add annotations and markers to the plot for highlighting important events.
- **User-Friendly Interface**: Easy-to-use interface with buttons for loading files, plotting signals, and clearing plots.
- **Enhanced Signal Selection**: Select and clear signals with ease, allowing for dynamic plotting.

### Usage

- Run the GUI application:
  ```
  python gui/gui_main.py
  ```
- Load the DBC and log files using the provided buttons.
- Select the signals you want to plot from the list.
- Click the "Plot Signals" button to visualize the selected signals.
- Use the interactive features to zoom, pan, and analyze the plots.

### Example Command
  ```
  python gui/gui_main.py
  ```

### GUI Working GIF    
<div align="center">
  <img src="https://github.com/user-attachments/assets/99054b12-e28b-470d-a788-66f846a47e8b" width="600" height="400" />
</div>

## Contributions

Feel free to contribute by adding new algorithms or improving the existing implementations. Please follow the contribution guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Contact

Kiran Jojare  
Embedded Software Engineer  
Phone: 720-645-6212  
Email: kijo7257@colorado.edu

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Happy Coding! 🚀
