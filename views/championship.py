import flet as ft
from api import fetch_results


def championship_view(page: ft.Page):
    results_general = {}
    driver_info = {}

    table = ft.DataTable(
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

    def load():
        table.rows.clear()
        results_general.clear()
        driver_info.clear()

        results = fetch_results()
        for r in results:
            results_general[r["driver"]] = results_general.get(r["driver"], 0) + r["points"]
            driver_info[r["driver"]] = r["team"]

        sorted_results = sorted(
            results_general.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for pos, (driver, points) in enumerate(sorted_results, start=1):
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(pos))),
                        ft.DataCell(ft.Text(driver)),
                        ft.DataCell(ft.Text(driver_info[driver])),
                        ft.DataCell(ft.Text(str(points))),
                    ]
                )
            )

        page.update()

    load()

    return ft.Column(
        [
            ft.Text("Championship Results", size=24, weight="bold"),
            ft.Divider(),
            table,
        ],
        expand=True,
    )
