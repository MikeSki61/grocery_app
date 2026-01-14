
def load_stylesheet():
    return """
    QWidget {
        background-color: #303830;
        color: #CBE3CA;
        font-family: Arial, sans-serif;
    }

    QPushButton {
        background-color: #47B840;
        color: #303830;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #4B7848;
    }

    QRadioButton {
        color: #CBE3CA;
        padding: 5px;
    }

    QTableWidget {
        background-color: #CBE3CA;  
        border: 1px solid #633951;
        color: #303830;
        padding: 10px;
    }

    QLineEdit {
        background-color: #CBE3CA;
        color: #303830;
        border: 1px solid #633951;
        padding: 5px;
        border-radius: 3px;
    }

    QComboBox {
        background-color: #303830;  
        color: #CBE3CA;
        padding: 5px;
    }

        QHeaderView::section {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 4px;
        border: 1px solid #3E3E3E;
    }
    """

