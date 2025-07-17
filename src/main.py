import flet as ft
from export import export_to_excel

# Currency list
currencies = ["USD", "RUB"]


def main(page: ft.Page):
    page.title = "Калькулятор стоимости сайта"
    page.padding = 32
    page.spacing = 32
    page.scroll = "auto"

    pages_column = ft.Column(spacing=32)

    # POPUP MENU
    about_dlg = ft.AlertDialog(
        title=ft.Text("Website Calculator App"),
        content=ft.Text("Copyright (C) 2025, srkdesign"),
        on_dismiss=lambda e: print("Dialog dismissed"),
    )

    pb_about = ft.PopupMenuItem(
        icon="INFO", text="О приложении", on_click=lambda e: page.open(about_dlg)
    )

    def open_website(e):
        page.launch_url("https://srkdesign.pro")

    pb_website = ft.PopupMenuItem(icon="WEB", text="Сайт автора", on_click=open_website)

    pb = ft.PopupMenuButton(
        items=[
            pb_website,
            pb_about,
        ]
    )

    grand_total_text = ft.Text("Итоговая стоимость сайта: 0.00 USD")

    all_pages_data = []

    # Currencies
    options = [ft.DropdownOption(currency) for currency in currencies]

    def on_currency_change(e):
        selected_currency = currency_dropdown.value
        section_bp.suffix_text = selected_currency
        page_bp.suffix_text = selected_currency
        page.update()

    currency_dropdown = ft.Dropdown(
        label="Валюта",
        options=options,
        value=currencies[1],
        on_change=on_currency_change,
    )

    # Basic Prices
    section_bp = ft.TextField(
        value=1000, label="Блок", suffix_text=currency_dropdown.value, expand=True
    )
    page_bp = ft.TextField(
        value=1500, label="Страница", suffix_text=currency_dropdown.value, expand=True
    )

    def add_page(e=None):
        subrows = []

        page_name_field = ft.TextField(
            label="Название страницы",
            value=str(f"Страница {len(pages_column.controls) + 1}"),
            expand=True,
        )

        subrow_count = ft.Text("Кол-во блоков: 0")
        total_cost = ft.Text("Итого: 0 USD")
        subrow_column = ft.Column(spacing=5)

        def get_base_price():
            try:
                return float(section_bp.value)
            except ValueError:
                return 0

        def update_summary():
            count = len(subrows)
            currency = currency_dropdown.value
            total = 0

            for row in subrows:
                try:
                    difficulty = float(row["difficulty"].value)
                except (ValueError, AttributeError):
                    difficulty = 0

                price = get_base_price() * difficulty
                row["price_text"].value = f"{price:.2f} {currency}"
                total += price

            subrow_count.value = f"Кол-во блоков: {count}"
            total_cost.value = (
                f"Итого: {max(total, float(page_bp.value)):.2f} {currency}"
            )
            calculate_grand_total()
            page.update()

        def add_subrow(e=None):
            title = ft.TextField(label="Название блока", expand=True)
            desc = ft.TextField(label="Описание", expand=True)
            difficulty = ft.TextField(
                label="Сложность", expand=True, on_change=lambda e: update_summary()
            )
            price_text = ft.Text("0.00", width=100)

            row_data = {
                "title": title,
                "description": desc,
                "difficulty": difficulty,
                "price_text": price_text,
            }

            subrows.append(row_data)

            delete_subrow_btn = ft.IconButton(
                icon="DELETE",
                tooltip="Удалить блок",
                on_click=lambda e, rd=row_data: delete_subrow(rd),
            )

            subrow_row = ft.Row(
                [title, desc, difficulty, price_text, delete_subrow_btn], spacing=16
            )
            row_data["row_control"] = subrow_row

            subrow_column.controls.append(subrow_row)
            update_summary()

        def delete_subrow(row_data):
            if row_data in subrows:
                subrows.remove(row_data)
                subrow_column.controls.remove(row_data["row_control"])
                update_summary()

        def delete_page(title, page_data):
            if title in pages_column.controls:
                pages_column.controls.remove(title)
                if page_data in all_pages_data:
                    all_pages_data.remove(page_data)
                page.update()

        section_bp.on_change = lambda e: update_summary()
        page_bp.on_change = lambda e: update_summary()
        currency_dropdown.on_change = lambda e: update_summary()
        add_subrow_btn = ft.ElevatedButton(
            icon="POST_ADD", text="Добавить блок", on_click=add_subrow
        )

        page_tile = ft.ExpansionTile(
            title=ft.Text(page_name_field.value),
            controls=[
                ft.Container(
                    expand=True,
                    margin=ft.margin.only(top=16, bottom=16),
                    border=None,
                    shadow=None,
                    bgcolor=None,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                expand=True,
                                controls=[
                                    page_name_field,
                                    ft.IconButton(
                                        icon="DELETE_FOREVER",
                                        tooltip="Удалить страницу",
                                        on_click=lambda e: delete_page(
                                            page_tile, page_data
                                        ),
                                    ),
                                ],
                            ),
                            subrow_column,
                            ft.Row(
                                controls=[
                                    add_subrow_btn,
                                    ft.Row([subrow_count, total_cost], spacing=30),
                                ]
                            ),
                        ]
                    ),
                )
            ],
            initially_expanded=True,
        )

        pages_column.controls.append(page_tile)
        page.update()

        page_data = {
            "name_field": page_name_field,
            "base_price": section_bp,
            "subrows": subrows,
        }

        all_pages_data.append(page_data)

        # Add default subrows
        for _ in range(1):
            add_subrow()

    def calculate_grand_total():
      total = 0.0

      for page_data in all_pages_data:

        sub_total = 0.0

        try:
          base_price = float(section_bp.value)
        except ValueError:
          base_price = 0.0

        try:
          min_page_price = float(page_bp.value)
        except ValueError:
          min_page_price = 0.0

        for row in page_data["subrows"]:
          try:
            difficulty = float(row["difficulty"].value)
          except (ValueError, AttributeError):
             difficulty = 0.0
          sub_total += base_price * difficulty

          total += max(sub_total, min_page_price)

      grand_total_text.value = f"Итоговая стоимость сайта: {total:.2f} {currency_dropdown.value}"

      page.update()

    progress_bar = ft.ProgressBar(visible=True, value=0)
    progress_text = ft.Text("Готово к экспорту")

    def export_progress():
      progress_bar.value = None
      progress_text.value = "Экспортируется..."
      page.update()

      try:
        export_to_excel(
          all_pages_data=all_pages_data,
          section_bp=section_bp,
          page_bp=page_bp,
          currency_code=currency_dropdown.value
        )
        progress_text.value = "Экспорт завершен"
      except Exception as ex:
        progress_text.value = f"Ошибка: {ex}"
      finally:
         progress_bar.value = 100
         page.update()
    
    layout = ft.Row(
      expand=True,
      controls=[
        ft.Column(
          expand=True,
          width=page.width,
          spacing=32,
          controls=[
            ft.Row(
              expand=True,
              width=page.width,
              controls=[currency_dropdown, section_bp, page_bp, pb],
            ),
            ft.Container(
              expand=True,
              content=pages_column,
            ),
            ft.Row(
              spacing=16,
              controls=[
                ft.ElevatedButton(
                  icon="NOTE_ADD", text="Добавить страницу", on_click=add_page
                ),
                ft.ElevatedButton(
                  icon="TABLE_VIEW_OUTLINED",
                  text="Экспортировать в Excel",
                  on_click=lambda e: export_progress()
                ),
              ]
            ),
            grand_total_text,
            ft.Container(expand=True),
            ft.Column(
              horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              controls=[
                progress_bar,
                progress_text
              ]
            )
          ]
        )
      ]
    )

    page.add(layout)

    add_page()


# Entry point
if __name__ == "__main__":
    ft.app(target=main)
