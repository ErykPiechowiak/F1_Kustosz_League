import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"
TOKEN = "kustosze"


def fetch_results():
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(
        f"{API_URL}/results",
        headers=headers,
        timeout=5
    )

    response.raise_for_status()
    return response.json()


def main(page: ft.Page):
    results_general = {}
    driver_info = {}


    page.title = "F1 Kustosz League"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    table_general_results = ft.DataTable(
    border=ft.Border.all(1, ft.Colors.GREY_400),
    border_radius=8,
    vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
    horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
    columns=[
        ft.DataColumn(ft.Text("Pos", weight="bold")),
        ft.DataColumn(ft.Text("Driver", weight="bold")),
        ft.DataColumn(ft.Text("Team", weight="bold")),
        ft.DataColumn(ft.Text("Points", weight="bold")),
    ],
    rows=[],
    )   

    def load_results(e=None):
        table_general_results.rows.clear()

        try:
            results = fetch_results()
            for r in results:
                if r['driver'] in results_general:
                    results_general[r['driver']] += r['points']
                else:
                    driver_info[r['driver']] = r['team']
                    results_general[r['driver']] = r['points']

            results_general_sorted = sorted(results_general.items(),
                                            key=lambda item: item[1],  # value = punkty
                                            reverse=True
                                        )
            position = 1
            for pair in results_general_sorted:
                    table_general_results.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(position))),
                            ft.DataCell(ft.Text(pair[0])), #pair[0] -> driver name
                            ft.DataCell(ft.Text(driver_info[pair[0]])), #driver team
                            ft.DataCell(ft.Text(str(pair[1]))), #pair[1] -> points
                            ]
                        )
                     )
                    position+=1


        except Exception as ex:
            table_general_results.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("—")),
                        ft.DataCell(ft.Text(f"Błąd: {ex}", color="red")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )

        page.update()


    page.add(
        ft.Row(
            [
                ft.Text("Championship Results", size=24, weight="bold"),
                ft.Button(
                    content="Odśwież",
                    on_click=load_results,
                    icon=ft.Icons.REFRESH
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        ft.Divider(),
        table_general_results,
    )


    # załaduj dane przy starcie
    load_results()


ft.run(main=main)