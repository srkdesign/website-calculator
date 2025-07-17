import flet as ft
import pandas as pd
import os

data_rows = []

currencies = [
    "USD",
    "RUB",
]

def create_workbook(filename="website-calculation.xlsx"):
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [30, 25, 35],
        "Country": ["USA", "Canada", "UK"]
    }
    df = pd.DataFrame(data)
    filepath = os.path.join(os.getcwd(), filename)
    df.to_excel(filepath, index=False, engine="xlsxwriter")

def main(page: ft.Page):
    page.title = "Website Calculator"

    options = [ft.DropdownOption(currency) for currency in currencies]

    def on_currency_change(e):
        selected = currency_dropdown.value
        section_price.suffix_text = selected
        page_price.suffix_text = selected
        page.update()

    currency_dropdown = ft.Dropdown(label="Валюта", options=options, value=currencies[1], on_change=on_currency_change)

    section_price = ft.TextField(value=1000, label="Блок", suffix_text=currency_dropdown.value, expand=True)
    page_price = ft.TextField(value=1500, label="Страница", suffix_text=currency_dropdown.value, expand=True)
    
    discount_percent = ft.TextField(expand=True, value=10, label="Скидка", suffix_text="%")
    output = ft.Text()

    def generate_file(e):
        try:
            create_workbook()
            output.value = "File generated"
        except Exception as ex:
            output.value = f"Error: {str(ex)}"
        page.update()

    btn = ft.ElevatedButton(text="Generate", on_click=generate_file)
    layout = ft.Column(alignment=ft.alignment.top_left, spacing=32, controls=[ft.Row(expand=True, width=page.width, controls=[currency_dropdown, section_price, page_price]), ft.Row(expand=True, controls=[discount_percent])])
    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
