from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Signal
from website_calc.widgets.section import Section

class Page(QWidget):
  changed = Signal()
  deleted = Signal(object)

  def __init__(self, section_bp_getter, page_bp_getter, currency_getter,parent=None):
    super().__init__(parent)

    self.section_bp_getter = section_bp_getter
    self.page_bp_getter = page_bp_getter
    self.currency_getter = currency_getter

    self.sections = []

    self.title = QLineEdit("Новая страница")
    self.section_count_label = QLabel("Кол-во блоков: 0")
    self.total_price_label = QLabel("Итого: 0.00")

    self.add_section_btn = QPushButton("Добавить блок")
    self.add_section_btn.clicked.connect(self.add_section)

    self.delete_page_btn = QPushButton("Удалить страницу")
    self.delete_page_btn.clicked.connect(lambda: self.deleted.emit(self))

    info_row = QHBoxLayout()
    info_row.addWidget(self.title)
    info_row.addWidget(self.delete_page_btn)

    btn_row = QVBoxLayout()
    btn_row.addWidget(self.add_section_btn)
    btn_row.addWidget(self.section_count_label)
    btn_row.addWidget(self.total_price_label)

    self.section_layout = QVBoxLayout()

    layout = QVBoxLayout()
    layout.addLayout(info_row)
    layout.addLayout(self.section_layout)
    layout.addLayout(btn_row)

    self.setLayout(layout)
    self.add_section()

  def add_section(self):
    section = Section()

    section.changed.connect(self.recalc)
    section.deleted.connect(self.remove_section)

    self.sections.append(section)
    self.section_layout.addWidget(section)

    self.recalc()

  def remove_section(self, section):
    self.sections.remove(section)
    section.setParent(None)
    section.deleteLater()
    self.recalc()

  def recalc(self):
    total = 0.0
    section_bp = self.section_bp_getter()
    page_bp = self.page_bp_getter()
    currency = self.currency_getter()

    for section in self.sections:
      difficulty = section.get_difficulty()
      price = section_bp * difficulty
      section.set_price(price, currency)
      total += price

    total = max(total, page_bp)

    self.total_price_label.setText(f"Итого: {total:.2f} {currency}")
    self.section_count_label.setText(f"Кол-во блоков: {len(self.sections)}")

    self.changed.emit()

  def get_total(self):
    total = 0.0
    section_bp = self.section_bp_getter()
    page_bp = self.page_bp_getter()

    for section in self.sections:
      difficulty = section.get_difficulty()
      total += section_bp * difficulty

    return max(total, page_bp)

