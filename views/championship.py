import flet as ft
from api import fetch_results


def championship_view(page: ft.Page):
#-------------------------------- DECLARATIONS-------------------------------------------

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
        #Load championship results
        results_general.clear() 
        driver_info.clear()

        results = fetch_results()
        #-------------------------------- DRIVERS CHAMPIONSHIP VIEW -------------------------------------------
        if dropdown_championship.value == "Drivers":
            table.rows.clear()
            table.columns = [
                ft.DataColumn(ft.Text("Pos", weight="bold")),
                ft.DataColumn(ft.Text("Driver", weight="bold")),
                ft.DataColumn(ft.Text("Team", weight="bold")),
                ft.DataColumn(ft.Text("Points", weight="bold"))
            ]
            for r in results:
                if str(r["season"]) == dropdown_season.value:
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
        #-------------------------------- TEAMS CHAMPIONSHIP VIEW -------------------------------------------
        else:
            for r in results:
                if str(r["season"]) == dropdown_season.value:
                    results_general[r["team"]] = results_general.get(r["team"], 0) + r["points"]

            sorted_results = sorted(
                results_general.items(),
                key=lambda x: x[1],
                reverse=True
            )

            table.rows.clear()
            table.columns = [
                ft.DataColumn(ft.Text("Pos", weight="bold")),
                ft.DataColumn(ft.Text("Team", weight="bold")),
                ft.DataColumn(ft.Text("Points", weight="bold"))
            ]


            for pos, (team, points) in enumerate(sorted_results, start=1):
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(pos))),
                            ft.DataCell(ft.Text(team)),
                            ft.DataCell(ft.Text(str(points))),
                        ]
                    )
                )

        page.update()
    
    dropdown_championship = ft.Dropdown(label="Select championship",on_select=load)
    dropdown_season = ft.Dropdown(label="Select season",on_select=load)



    def load_options():
        #results = fetch_results()
        seasons = ["1","2"]
        dropdown_season.options = [ft.dropdown.Option(r) for r in seasons]
        championships = ["Drivers", "Constructors"]
        dropdown_championship.options = [ft.dropdown.Option(r) for r in championships]
        page.update()

    load_options()
    #load()

    return ft.Column(
        expand=True,
        controls=[
            ft.Text("Championship Results", size=24, weight="bold"),

            ft.Row(
                controls=[
                    dropdown_championship,
                    dropdown_season,
                ],
                spacing=100
            ),

            ft.Divider(),
            table,

            ft.Container(
                content=ft.Text(
                    "Made by erzkoy",
                    size=12,
                    italic=True,
                    opacity=0.6,
                ),
                padding=20,
            ),
        ],
    )

