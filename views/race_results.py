import flet as ft
from api import fetch_results


def race_results_view(page: ft.Page):

    def load_results(e):
        race = dropdown.value
        table.rows.clear()
        for r in fetch_results():
            if r['track_name'] == race:
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(r["position"]))),
                            ft.DataCell(ft.Text(r["driver"])),
                            ft.DataCell(ft.Text(r["team"])),
                            ft.DataCell(ft.Text(r["fastest_lap"])),
                            ft.DataCell(ft.Text(r["time"])),
                            ft.DataCell(ft.Text(str(r["points"]))),
                        ]
                    )
                )
        page.update()
        
    
    dropdown = ft.Dropdown(label="Select race",on_select=load_results)

    table = ft.DataTable(
        border=ft.Border.all(1, ft.Colors.GREY_400),
        border_radius=8,
        vertical_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        columns=[
            ft.DataColumn(ft.Text("Pos", weight="bold")),
            ft.DataColumn(ft.Text("Driver", weight="bold")),
            ft.DataColumn(ft.Text("Team", weight="bold")),
            ft.DataColumn(ft.Text("Fastest Lap", weight="bold")),
            ft.DataColumn(ft.Text("Time", weight="bold")),
            ft.DataColumn(ft.Text("Points", weight="bold")),
        ],
        rows=[],
    )

    def load_races():
        results = fetch_results()
        races = sorted({r["track_name"] for r in results})
        dropdown.options = [ft.dropdown.Option(r) for r in races]
        page.update()

    

    load_races()

    return ft.Column(
        [
            ft.Text("Race results", size=24, weight="bold"),
            dropdown,
            ft.Divider(),
            table,
        ],
        expand=True,
    )
