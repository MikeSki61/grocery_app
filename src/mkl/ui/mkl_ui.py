from PyQt5 import QtWidgets, QtCore, QtGui
from mkl import constants
from mkl import mk_core
from mkl import utils

class GroceryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.grocery_app = mk_core.GroceryList()

        self.mode ="loading"
        
        self.setWindowTitle("Mk Grocery List")
        self.setGeometry(100, 100, 600, 900)

        # Layouts
        self.main_layout = QtWidgets.QVBoxLayout()
        self.sort_layout = QtWidgets.QHBoxLayout()

        # Inputs
        self.name_input = QtWidgets.QLineEdit(self, placeholderText="Name")
        self.store_input = QtWidgets.QLineEdit(self, placeholderText="Store")
        self.cost_input = QtWidgets.QLineEdit(self, placeholderText="Cost")
        self.amount_input = QtWidgets.QLineEdit(self, placeholderText="Amount")
        self.priority_input = QtWidgets.QLineEdit(self, placeholderText="Priority")

        # Validators
        self.text_only_validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression("[A-Za-z\\s]+")
        )
        self.float_validator = QtGui.QDoubleValidator(0.0, 9999.99, 2)
        self.integer_validator = QtGui.QIntValidator(1, 9999)
        self.priority_validator = QtGui.QIntValidator(1, 5, self)

        self.name_input.setValidator(self.text_only_validator)
        self.store_input.setValidator(self.text_only_validator)
        self.cost_input.setValidator(self.float_validator)
        self.amount_input.setValidator(self.integer_validator)
        self.priority_input.setValidator(self.priority_validator)

        # Buttons
        self.add_button = QtWidgets.QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.delete_button = QtWidgets.QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_item)
        self.sort_button = QtWidgets.QPushButton("Sort")
        self.sort_button.clicked.connect(self.sort_items)
        self.export_button = QtWidgets.QPushButton("Export Selected Items")
        self.export_button.clicked.connect(self.export_selected_items)

        # Radio Buttons
        self.ascending_radio = QtWidgets.QRadioButton("asc")
        self.descending_radio = QtWidgets.QRadioButton("desc")
        self.ascending_radio.setChecked(True)

        self.sort_order_group = QtWidgets.QButtonGroup()
        self.sort_order_group.addButton(self.ascending_radio)
        self.sort_order_group.addButton(self.descending_radio)

        # Sort Combo Box
        self.sort_combo_box = QtWidgets.QComboBox()
        self.populate_combo_box()

        # Search field
        self.search_input = QtWidgets.QLineEdit(self, placeholderText="Search by Name")
        self.search_input.textChanged.connect(self.search_items)

        # Table Widget
        self.items_table = QtWidgets.QTableWidget()
        self.items_table.setColumnCount(6)
        self.items_table.setHorizontalHeaderLabels(
            ["Name", "Store", "Cost ($)", "Amount", "Priority", "Buy"]
        )
        self.items_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.items_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.items_table.setShowGrid(False)
        self.items_table.itemSelectionChanged.connect(self.item_selected)
        self.items_table.itemChanged.connect(self.on_items_changed)

        # Sort Layout
        self.sort_layout.addWidget(self.sort_combo_box)
        self.sort_layout.addWidget(self.ascending_radio)
        self.sort_layout.addWidget(self.descending_radio)
        self.sort_layout.addWidget(self.sort_button)

        # Main Layout
        self.main_layout.addWidget(self.name_input)
        self.main_layout.addWidget(self.store_input)
        self.main_layout.addWidget(self.cost_input)
        self.main_layout.addWidget(self.amount_input)
        self.main_layout.addWidget(self.priority_input)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.sort_layout)
        self.main_layout.addWidget(self.search_input)
        self.main_layout.addWidget(self.items_table)
        self.main_layout.addWidget(self.export_button)
        self.setLayout(self.main_layout)

        self.reload_ui()
        
    def run(self):
        self.show()

    def add_item(self):
        name = constants.NAME_DEFAULT
        store = constants.STORE_DEFAULT
        cost = constants.COST_DEFAULT
        amount = constants.AMOUNT_DEFAULT
        priority = constants.PRIORITY_DEFAULT
        buy = constants.BUY_DEFAULT

        if self.name_input.text():
            name = str(self.name_input.text())

        if self.store_input.text():
            store = str(self.store_input.text())

        if self.cost_input.text():
            cost = float(self.cost_input.text())

        if self.amount_input.text():
            amount = int(self.amount_input.text())

        if self.priority_input.text():
            priority = int(self.priority_input.text())

        self.grocery_app.add_item(name, store, cost, amount, priority, buy)
        utils.show_warning(title="SUCCESS", msg=f"{name} was added")
    
        self.reload_ui()

    def delete_item(self, name):
        selected_items = self.items_table.selectedItems()
        if selected_items:
            row = self.items_table.currentRow()
            name = str(self.items_table.item(row, 0).text())
            id = self.items_table.item(row, 0).data(QtCore.Qt.UserRole)
            self.items_table.removeRow(row)
            self.grocery_app.remove_item(name, id)   
            utils.show_warning(title="SUCCESS", msg=f"{name} was removed")

    def populate_combo_box(self):
        for attr in ["name", "store", "cost", "amount", "priority"]:
            self.sort_combo_box.addItem(attr)
        self.sort_combo_box.setCurrentText("name")

    def reload_ui(self):
        self.mode = "loading"

        # Clear Input Fields
        self.name_input.clear()
        self.store_input.clear()
        self.cost_input.clear()
        self.amount_input.clear()
        self.priority_input.clear()

        # Reload The Table
        self.items_table.setRowCount(0)

        if self.grocery_app.grocery_list:
            for item in self.grocery_app.grocery_list:
                row_position = self.items_table.rowCount()
                self.items_table.insertRow(row_position)

                #Add the rest of the item attributes
                self.items_table.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(item.name)
                )
                self.items_table.setItem(
                    row_position, 1, QtWidgets.QTableWidgetItem(item.store)
                )
                self.items_table.setItem(
                    row_position, 2, QtWidgets.QTableWidgetItem(f"{item.cost}")
                )
                self.items_table.setItem(
                    row_position, 3, QtWidgets.QTableWidgetItem(str(item.amount))
                )
                self.items_table.setItem(
                    row_position, 4, QtWidgets.QTableWidgetItem(str(item.priority))
                )

                #Add checkbox in the first column
                checkbox_item = QtWidgets.QTableWidgetItem()
                checkbox_item.setFlags(
                    QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
                )
                if item.buy == True:
                    checkbox_item.setCheckState(QtCore.Qt.Checked)
                else:
                    checkbox_item.setCheckState(QtCore.Qt.Unchecked)

                self.items_table.setItem(row_position, 5, checkbox_item)

                # Set the data for row 6, keep it hidden
                self.items_table.item(row_position, 0).setData(
                    QtCore.Qt.UserRole, item.id
                )

        self.mode = "user"
                
    def on_items_changed(self, item):
        if self.mode == "loading":
            return

        row = item.row()
        name = str(self.items_table.item(row, 0).text())
        store = str(self.items_table.item(row, 1).text())
        cost = float(self.items_table.item(row, 2).text())
        amount = int(self.items_table.item(row, 3).text())
        priority = int(self.items_table.item(row, 4).text())

        checkbox_item = self.items_table.item(row, 5)

        if checkbox_item.checkState() == QtCore.Qt.Checked:
            buy = True
        else:
            buy = False

        id = self.items_table.item(row, 0).data(QtCore.Qt.UserRole)

        self.grocery_app.edit_item(name, store, cost, amount, priority, buy, id)

        self.reload_ui()

    def item_selected(self):
        selected_items = self.items_table.selectedItems()
        if selected_items:
            row = self.items_table.currentRow()
            self.name_input.setText(self.items_table.item(row, 0).text())
            self.store_input.setText(self.items_table.item(row, 1).text())
            self.cost_input.setText(
                self.items_table.item(row, 2).text().replace("$", "")
            )
            self.amount_input.setText(self.items_table.item(row, 3).text())
            self.priority_input.setText(self.items_table.item(row, 4).text())

    def sort_items(self):
        if self.ascending_radio.isChecked():
            reverse = False
        else:
            reverse = True
        self.grocery_app.sort_items(self.sort_combo_box.currentText(), reverse=reverse)
        self.reload_ui()

    def search_items(self):
        search_term = self.search_input.text().lower()
        self.items_table.setRowCount(0)

        matching_items = self.grocery_app.search_item_name(search_term)

        self.mode = "loading"
        for item in matching_items:
            row_position = self.items_table.rowCount()
            self.items_table.insertRow(row_position)

            self.items_table.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(item.name)
            )
            self.items_table.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(item.store)
            )
            self.items_table.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(f"{item.cost}")
            )
            self.items_table.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(item.amount))
            )
            self.items_table.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(item.priority))
            )
        self.mode = "user"

    def export_selected_items(self):
        self.grocery_app.export_items()





