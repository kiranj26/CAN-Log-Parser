import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, 
                             QPushButton, QListWidget, QHBoxLayout, QSplitter, QLabel, 
                             QComboBox, QInputDialog, QGridLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import parse_dbc, parse_log

class CANLogParserGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN Log Parser")

        self.dbc_file = None
        self.log_file = None
        self.db = None
        self.parsed_data = None
        self.subplots = []

        self.initUI()

    def initUI(self):
        """
        Initialize the GUI layout and components.
        """
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Toolbar for actions
        toolbar = QHBoxLayout()

        # Add buttons for loading files, clearing plots, and exporting plots
        load_dbc_btn = QPushButton('Load DBC File')
        load_log_btn = QPushButton('Load Log File')
        clear_plots_btn = QPushButton('Clear Plots')
        export_plot_btn = QPushButton('Export Plot')

        load_dbc_btn.clicked.connect(self.load_dbc_file)
        load_log_btn.clicked.connect(self.load_log_file)
        clear_plots_btn.clicked.connect(self.clear_plots)
        export_plot_btn.clicked.connect(self.export_plot)

        toolbar.addWidget(load_dbc_btn)
        toolbar.addWidget(load_log_btn)
        toolbar.addWidget(clear_plots_btn)
        toolbar.addWidget(export_plot_btn)

        main_layout.addLayout(toolbar)

        # Splitter for controls and plotting area
        splitter = QSplitter(Qt.Horizontal)

        # Left panel for signal selection and controls
        controls_layout = QVBoxLayout()
        self.signal_list = QListWidget()
        self.signal_list.setSelectionMode(QListWidget.MultiSelection)

        self.plot_button = QPushButton('Plot Signals')
        self.clear_selection_button = QPushButton('Clear Selection')
        self.plot_button.clicked.connect(self.plot_signals)
        self.clear_selection_button.clicked.connect(self.clear_selection)

        controls_layout.addWidget(QLabel("Select Signals:"))
        controls_layout.addWidget(self.signal_list)
        controls_layout.addWidget(self.clear_selection_button)
        controls_layout.addWidget(self.plot_button)

        controls_container = QWidget()
        controls_container.setLayout(controls_layout)
        splitter.addWidget(controls_container)

        # Right panel for plotting area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)

        plot_container = QWidget()
        plot_container.setLayout(plot_layout)
        splitter.addWidget(plot_container)

        splitter.setSizes([200, 800])
        main_layout.addWidget(splitter)

        self.setCentralWidget(main_widget)
        self.init_subplots(6)

    def init_subplots(self, num_subplots):
        """
        Initialize a specified number of subplots.
        """
        self.figure.clear()
        self.subplots = []
        for i in range(num_subplots):
            ax = self.figure.add_subplot(num_subplots, 1, i + 1)
            self.subplots.append(ax)
        self.canvas.draw()

    def load_dbc_file(self):
        """
        Load the DBC file and parse it.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load DBC File", "", "DBC Files (*.dbc);;All Files (*)", options=options)
        if file_name:
            self.dbc_file = file_name
            self.db = parse_dbc(self.dbc_file)
            if self.db:
                self.signal_list.clear()
                for message in self.db.messages:
                    for signal in message.signals:
                        self.signal_list.addItem(signal.name)

    def load_log_file(self):
        """
        Load the log file and parse it.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Log File", "", "Log Files (*.txt);;All Files (*)", options=options)
        if file_name:
            self.log_file = file_name
            self.parsed_data = parse_log(self.db, self.log_file)

    def plot_signals(self):
        """
        Plot the selected signals based on user input.
        """
        selected_signals = [item.text() for item in self.signal_list.selectedItems()]
        if not selected_signals or not self.parsed_data:
            return

        for i, signal_name in enumerate(selected_signals):
            subplot_index = self.select_subplot()
            ax = self.subplots[subplot_index]

            timestamps = []
            values = []
            for data in self.parsed_data:
                for signal in data['signals']:
                    s_name, s_value, s_timestamp = signal
                    if s_name == signal_name:
                        timestamps.append(float(s_timestamp) / 1000)  # Convert to seconds
                        values.append(float(s_value))

            ax.plot(timestamps, values, label=signal_name)
            ax.set_xlabel('Time (s)', fontsize=8)
            ax.set_ylabel('Value', fontsize=8)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.grid(True)
            ax.legend(fontsize=6)
        self.canvas.draw()

    def select_subplot(self):
        """
        Select a subplot index for plotting based on user input.
        """
        subplot_index, ok = QInputDialog.getInt(self, "Select Subplot", "Enter subplot number (1 to 6):", 1, 1, len(self.subplots), 1)
        return subplot_index - 1 if ok else 0

    def clear_selection(self):
        """
        Clear the selected signals in the list.
        """
        self.signal_list.clearSelection()

    def clear_plots(self):
        """
        Clear all the plots.
        """
        self.figure.clear()
        self.init_subplots(6)
        self.canvas.draw()

    def export_plot(self):
        """
        Export the current plot as an image file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Plot", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_name:
            self.figure.savefig(file_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CANLogParserGUI()
    gui.show()
    sys.exit(app.exec_())
