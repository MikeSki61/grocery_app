from PyQt5 import QtWidgets


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, store_default: str = "", tax_rate: float = 0.08):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        # Line Edit
        self.store_edit = QtWidgets.QLineEdit(self)
        self.store_edit.setText(store_default)

        # Spin Box
        self.tax_spin = QtWidgets.QDoubleSpinBox(self)
        self.tax_spin.setRange(0.0, 100.0)
        self.tax_spin.setDecimals(2)
        self.tax_spin.setSingleStep(0.1)
        self.tax_spin.setSuffix(" %")
        self.tax_spin.setValue(tax_rate * 100.0)

        # Layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Default store:", self.store_edit)
        form_layout.addRow("Tax rate:", self.tax_spin)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(buttons)

    def get_settings(self):
        store_default = self.store_edit.text().strip()
        tax_rate_decimal = self.tax_spin.value() / 100.0
        return {
            "store_default": store_default,
            "tax_rate": tax_rate_decimal,
        }
