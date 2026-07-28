import sys

from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from barrier_calc import barrier_inputs, sliding_check




class BarrierCalculatorWindow(QMainWindow):
    """Main window for the Barrier Calculator application."""
    def __init__(self) -> None:
        """Initializes the main window."""
        super().__init__()

        self.setWindowTitle("Temporary Barrier Stability Calculator")
        self.resize(900,650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout(central_widget)

        input_panel = self.create_input_panel()
        fixed_params_panel = self.fixed_parameters_panel()
        result_panel = self.create_result_panel()

        main_layout.addWidget(input_panel, 0, 0)
        main_layout.addWidget(fixed_params_panel, 1, 0)
        main_layout.addWidget(result_panel, 0, 1, 2, 1)

    def create_number_input(
            self,
            minimum: float,
            maximum: float,
            value: float,
            decimals: int=3,
    ) -> QDoubleSpinBox:
        """Creates a number input field.

        Args:
            minimum (float): The minimum value for the input.
            maximum (float): The maximum value for the input.
            value (float): The default value for the input.
            decimals (int, optional): The number of decimal places. Defaults to 3.

        Returns:
            QDoubleSpinBox: The created number input field.
        """
        field = QDoubleSpinBox()
        field.setRange(minimum, maximum)
        field.setValue(value)
        field.setDecimals(decimals)
        field.setSingleStep(0.1)
        return field

    def create_input_panel(self) -> QGroupBox:
        """Creates the input panel for the application.

        Returns:
            QGroupBox: The created input panel.
        """
        group = QGroupBox("Assessment Inputs")
        layout = QFormLayout(group)

        self.water_depth_input = self.create_number_input(
            minimum=0.0,
            maximum=1.0,
            value=0.6,
            decimals=2,
        )

        self.mu_membrane_input = self.create_number_input(
            minimum=0.0,
            maximum=2.0,
            value=0.33,
            decimals=3,
        )

        self.mu_barrier_input = self.create_number_input(
            minimum=0.0,
            maximum=2.0,
            value=0.72,
            decimals=3,
        )

        self.mu_kentledge_input = self.create_number_input(
            minimum=0.0,
            maximum=2.0,
            value=0.40,
            decimals=3,
        )

        layout.addRow("Water Depth (m):", self.water_depth_input)
        layout.addRow("Membrane Friction Coefficient:", self.mu_membrane_input)
        layout.addRow("Barrier Friction Coefficient:", self.mu_barrier_input)
        layout.addRow("Kentledge Friction Coefficient:", self.mu_kentledge_input)

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)

        layout.addRow(calculate_button)

        return group

    def fixed_parameters_panel(self) -> QGroupBox:
        """Creates the fixed parameters panel for the application.

        Returns:
            QGroupBox: The created fixed parameters panel.
        """
        group = QGroupBox("Fixed Barrier Specifications")
        layout = QFormLayout(group)

        layout.addRow("Barrier width:", QLabel("1.0 m"))
        layout.addRow("Barrier angle:", QLabel("38.7°"))
        layout.addRow("Membrane width:", QLabel("2.0 m"))
        layout.addRow("Alpha:", QLabel("0.203"))
        layout.addRow("Barrier mass:", QLabel("26.5 kg"))
        layout.addRow("Slope height:", QLabel("0.72 m"))
        layout.addRow("Required FoS:", QLabel("1.5"))

        return group

    def create_result_panel(self) -> QGroupBox:
        """Creates the result panel for the application."""
        group = QGroupBox("Results")
        layout = QVBoxLayout(group)

        self.driving_force_label = QLabel("Driving Force (kN): -")
        self.resisting_force_label = QLabel("Total Resistance (kN): -")
        self.fos_label = QLabel("Sliding Factor of Safety: -")
        self.status_label = QLabel("Status: -")
        self.required_kentledge_label = QLabel("Required Kentledge Mass (kg): -")

        layout.addWidget(self.driving_force_label)
        layout.addWidget(self.resisting_force_label)
        layout.addWidget(self.fos_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.required_kentledge_label)
        layout.addStretch()

        return group



    def calculate(self) -> None:
        """Calculates the sliding check based on user inputs."""
        inputs = barrier_inputs(
            water_depth=self.water_depth_input.value(),
            mu_membrane_ground=self.mu_membrane_input.value(),
            mu_barrier_ground=self.mu_barrier_input.value(),
            mu_kentledge_ground=self.mu_kentledge_input.value(),
        )

        outputs = sliding_check(inputs)

        self.driving_force_label.setText(f"Driving Force (kN): {outputs.total_driving_force_kN:.3f}")
        self.resisting_force_label.setText(f"Total Resistance (kN): {outputs.resisting_force_kN:.3f}")
        self.fos_label.setText(f"Sliding Factor of Safety: {outputs.actual_fos:.3f}")
        if outputs.passes:
            self.status_label.setText("Status: PASS")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")

        else:
            self.status_label.setText("Status: FAIL")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.required_kentledge_label.setText(f"Required Kentledge Mass (kg): {outputs.required_kentledge_mass_kg:.0f}")

        return


def main() -> None:
    """Launches the barrier calculator application."""
    app = QApplication(sys.argv)
    window = BarrierCalculatorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


