"""
My first application
"""

import importlib.metadata
import sys

from website_calc.export import export_to_excel
from website_calc.widgets.currency_dropdown import CurrencyDropdown
from website_calc.widgets.base_price_field import BasePriceField
from website_calc.widgets.page import Page

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFileDialog
)
from PySide6.QtGui import QIcon

currencies = ["USD", "RUB"]

class Pages(QWidget):
  pass

class WebsiteCalc(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.init_ui()

  def init_ui(self):
    self.setWindowTitle("Website Calculator by srkdesign")
    self.resize(800,600)

    central = QWidget()
    self.setCentralWidget(central)
    self.layout = QVBoxLayout(central)

    self.currency_dropdown = CurrencyDropdown(currencies=currencies, default_currency="RUB")
    self.currency_dropdown.currency_changed.connect(self.on_currency_change)
    self.layout.addWidget(self.currency_dropdown)

    self.section_bp = BasePriceField(label="Блок:", default_value="1000")
    self.page_bp = BasePriceField(label="Страница:", default_value="1500")

    bp_row = QHBoxLayout()
    bp_row.addWidget(self.section_bp)
    bp_row.addSpacing(32)
    bp_row.addWidget(self.page_bp)

    self.layout.addLayout(bp_row)

    self.scroll_area = QScrollArea()
    self.scroll_area.setWidgetResizable(True)

    self.pages_container = QWidget()
    self.pages_layout = QVBoxLayout(self.pages_container)

    self.scroll_area.setWidget(self.pages_container)
    self.layout.addWidget(self.scroll_area)

    btn_layout = QVBoxLayout()
    self.add_page_btn = QPushButton("Добавить страницу")
    self.add_page_btn.clicked.connect(self.add_page)

    self.export_btn = QPushButton("Экспортировать в Excel")
    self.export_btn.clicked.connect(self.export_data)

    btn_layout.addWidget(self.add_page_btn)
    btn_layout.addWidget(self.export_btn)

    self.layout.addLayout(btn_layout)

    self.grand_total_label = QLabel("Итоговая стоимость: 0.00 RUB")
    self.layout.addWidget(self.grand_total_label)

    self.pages = []

    self.section_bp.changed.connect(self.update_all_pages)
    self.page_bp.changed.connect(self.update_all_pages)

    self.add_page()

    self.show()

  def on_currency_change(self, currency):
    self.section_bp.set_suffix(currency)
    self.page_bp.set_suffix(currency)
    self.calculate_total()

  def add_page(self):
    page = Page(section_bp_getter=self.section_bp.get_price, page_bp_getter=self.page_bp.get_price, currency_getter=self.currency_dropdown.current_currency)

    page.changed.connect(self.update_grand_total)
    page.deleted.connect(self.remove_page)

    self.pages.append(page)
    self.pages_layout.addWidget(page)
    self.update_grand_total()

  def remove_page(self, page):
    if page in self.pages:
      self.pages.remove(page)
      page.setParent(None)
      self.update_grand_total()

  def update_all_pages(self):
    for page in self.pages:
      page.update_prices()
    self.update_grand_total()

  def update_grand_total(self):
    total = 0.0
    currency = self.currency_dropdown.current_currency()

    for page in self.pages:
        total += page.get_total()

    self.grand_total_label.setText(f"Итоговая стоимость сайта: {total:.2f} {currency}")

  # def calculate_total(self):
  #   section_price = self.section_bp.get_price()
  #   page_price = self.page_bp.get_price()
  #   currency = self.currency_dropdown.current_currency()

  #   total = max(section_price, page_price)
  #   self.grand_total_label.setText(f"Итоговая стоимость сайта: {total:.2f} {currency}")

  def export_data(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "Сохранить расчет в Excel",
        "project_estimate.xlsx",
        "Excel Files (*.xlsx);;All Files (*)",
        options=options
    )

    if filename:
        # Make sure filename ends with .xlsx
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"

        export_to_excel(
          pages=self.pages,
          section_bp_field=self.section_bp.get_price,
          filename=filename,
          page_bp_field=self.page_bp.get_price,
          currency_code=self.currency_dropdown.current_currency,
        )
    print("Export logic triggered (to be implemented).")

def main():
  # Linux desktop environments use an app's .desktop file to integrate the app
  # in to their application menus. The .desktop file of this app will include
  # the StartupWMClass key, set to app's formal name. This helps associate the
  # app's windows to its menu item.
  #
  # For association to work, any windows of the app must have WMCLASS property
  # set to match the value set in app's desktop file. For PySide6, this is set
  # with setApplicationName().

  # Find the name of the module that was used to start the app
  app_module = sys.modules["__main__"].__package__
  # Retrieve the app's metadata
  metadata = importlib.metadata.metadata(app_module)

  QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])

  app = QtWidgets.QApplication(sys.argv)
  main_window = WebsiteCalc()
  sys.exit(app.exec())
