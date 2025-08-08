from PySide6.QtCore import Qt, Signal, QRegularExpression
from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QRegularExpressionValidator

class Section(QWidget):
  changed = Signal(object)
  deleted = Signal(object)

  def __init__(self, parent=None):
    super().__init__(parent)

    self.title = QLineEdit(placeholderText="Название блока")
    self.desc = QLineEdit(placeholderText="Описание")

    self.difficulty = QLineEdit(placeholderText="Сложность")
    validator = QRegularExpressionValidator(QRegularExpression(r"^(0|[1-5]|([1-5])/([1-5])|0?\.\d+)$"))
    self.difficulty.setValidator(validator)
    self.difficulty.textChanged.connect(lambda _: self.changed.emit(self))

    self.price_label = QLabel("0.00")

    self.delete_btn = QPushButton("Удалить")
    self.delete_btn.clicked.connect(self.on_delete)

    layout =  QHBoxLayout()
    layout.addWidget(self.title, stretch=1)
    layout.addWidget(self.desc, stretch=1)
    layout.addWidget(self.difficulty, stretch=1)
    layout.addWidget(self.price_label, stretch=1)
    layout.addWidget(self.delete_btn)
    # layout.setAlignment(Qt.AlignJustify)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)
    self.setLayout(layout)

  def on_delete(self):
    self.deleted.emit(self)

  def get_difficulty(self):
    try:
      return float(self.difficulty.text())
    except ValueError:
      return 0.0
    
  def set_price(self, price: float, currency: str):
    self.price_label.setText(f"{price:.2f} {currency}")