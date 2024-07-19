
# CAN Log Parser

# CAN-Log-Parser

![CI Workflow](https://github.com/<your-username>/CAN-Log-Parser/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/<your-username>/CAN-Log-Parser/branch/main/graph/badge.svg)](https://codecov.io/gh/<your-username>/CAN-Log-Parser)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/<your-project-token>)](https://www.codacy.com/gh/<your-username>/CAN-Log-Parser/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=<your-username>/CAN-Log-Parser&amp;utm_campaign=Badge_Grade)

This project is a CAN log parser that parses DBC files and CAN log files, and plots signal values over time.

## Features
- Parse DBC files
- Parse CAN log files
- Plot signal values

## Usage
### Parsing DBC Files
```bash
python src/parse_dbc.py path_to_dbc_file


This project is a tool to parse DBC formatted CAN log files and plot the signals.

## Features
- Parse DBC files to extract signal definitions
- Read and parse CAN log files
- Decode signals from CAN messages
- Plot the decoded signals

## Requirements
- Python 3.8+
- cantools
- matplotlib

## Installation
Clone the repository and install the required packages:

```bash
git clone https://github.com/your-username/CAN-Log-Parser.git
cd CAN-Log-Parser
pip install -r requirements.txt
```

## Usage
Place your DBC file and log file in the `data/` directory.

Run the main script:

```bash
python src/main.py
```

## Repository Structure
- `src/`: Contains the main scripts
  - `main.py`: Main script to run the tool
  - `can_parser.py`: Contains functions to parse CAN messages
  - `plot_signals.py`: Contains functions to plot signals
- `data/`: Directory to place your DBC and log files

## Example
An example DBC file and log file are provided in the `data/` directory.

## Dependencies
- `cantools`: A library for parsing DBC files and decoding CAN messages. It simplifies working with CAN databases and allows you to decode and encode CAN messages.
- `matplotlib`: A plotting library for Python and its numerical mathematics extension NumPy. It provides an object-oriented API for embedding plots into applications.
