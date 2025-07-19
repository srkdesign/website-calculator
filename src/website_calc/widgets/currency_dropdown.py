from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QComboBox,
)
from PySide6.QtCore import Signal

class CurrencyDropdown(QWidget):
  currency_changed = Signal(str)

  def __init__(self, currencies, default_currency=None, parent=None):
    super().__init__(parent)

    self.currencies = currencies
    self.dropdown = QComboBox()
    self.dropdown.addItems(self.currencies)

    if default_currency and default_currency in self.currencies:
      index = self.currencies.index(default_currency)
      self.dropdown.setCurrentIndex(index)

    label = QLabel("Валюта:")

    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(self.dropdown)
    layout.addStretch()

    self.setLayout(layout)

    self.dropdown.currentTextChanged.connect(self.on_currency_changed)

  def on_currency_changed(self, value):
    self.currency_changed.emit(value)

  def current_currency(self):
    return self.dropdown.currentText()
