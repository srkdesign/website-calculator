from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtCore import Signal

class BasePriceField(QWidget):
  changed = Signal(float)
  def __init__(self, label="Цена:", default_value="0", parent=None):
    super().__init__(parent)

    self.input = QLineEdit(default_value)

    layout = QHBoxLayout()
    layout.addWidget(QLabel(label))
    layout.addWidget(self.input)
    self.setLayout(layout)

  def get_price(self):
    try:
      return float(self.input.text())
    except ValueError:
      return 0.0
    
  def set_price(self, value):
    self.input.setText(str(value))

  def set_suffix(self, suffix):
    current_text = self.input.text()

    if " " in current_text:
      current_text = current_text.split()[0]
    self.input.setText(f"{current_text}")
