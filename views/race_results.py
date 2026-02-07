import flet as ft
from api import fetch_results


def race_results_view(page: ft.Page):

    def load_results(e):
        race = dropdown_race.value
        table.rows.clear()
        for r in fetch_results():
            if r['track_name'] == race and str(r['season']) == dropdown_season.value:
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

    def update_race_dropdown():
        table.rows.clear()
        results = fetch_results()
        results_selected_season = []
        for r in results:
            if str(r["season"]) == dropdown_season.value:
                results_selected_season.append(r)
        races = sorted({r["track_name"] for r in results_selected_season})
        dropdown_race.options = [ft.dropdown.Option(r) for r in races]   
    
    dropdown_race = ft.Dropdown(label="Select race",on_select=load_results)
    dropdown_season = ft.Dropdown(label="Select season",on_select=update_race_dropdown)

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



    def init_season_dropdown():
        #season dropdown
        seasons = ["1","2"]
        dropdown_season.options = [ft.dropdown.Option(r) for r in seasons]
        page.update()


    init_season_dropdown()

    return ft.Column(
        [
            ft.Text("GP results", size=24, weight="bold"),
                ft.Row(
                [
                    dropdown_season,
                    dropdown_race,
                ],
                spacing = 100
                ),
            ft.Divider(),
            table,
        ],
        expand=True,
    )
