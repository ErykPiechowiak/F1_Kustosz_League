import flet as ft
from api import fetch_results, fetch_quali_results



def race_results_view(page: ft.Page):
    #---------------------GLOBAL DECLARATIONS-----------------------
    mode = "race"
    #table declaration
    
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
    def load_results(e):
        race = dropdown_race.value
        table.rows.clear()
        if mode == "race":

            
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
        else:
            i = 1
            for r in fetch_quali_results():
                if r['track_name'] == race and str(r['season']) == dropdown_season.value:
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(i))),
                                ft.DataCell(ft.Text(r["driver"])),
                                ft.DataCell(ft.Text(r["team"])),
                                ft.DataCell(ft.Text(r["quali_time"])),
                            ]
                        )
                    )
                    i+=1
        page.update()

    #-----------------------DROPDOWN FUNCTIONS-----------------------------

    #dropdown functions 
    def update_race_dropdown(): 
        table.rows.clear()
        results = fetch_results()
    
        unique_races = {
            (r["round_nr"], r["track_name"])
            for r in results
            if str(r["season"]) == dropdown_season.value
        }
    
        # sortujemy po numerze rundy
        sorted_races = sorted(unique_races, key=lambda x: x[0])
    
        dropdown_race.options = [
            ft.dropdown.Option(f"{track_name}")
            for round_nr, track_name in sorted_races
        ]
    

    def init_season_dropdown():
        seasons = ["1","2"]
        dropdown_season.options = [ft.dropdown.Option(r) for r in seasons]
        page.update()

    #-----------------------SWITCH FUNCTIONS-----------------------------

    def switch_mode(e):
        nonlocal mode
        mode = e.control.selected[0]   # bo to lista
        print(mode)
        table.rows.clear()
        if mode == "race":
            table.columns = [
                ft.DataColumn(ft.Text("Pos", weight="bold")),
                ft.DataColumn(ft.Text("Driver", weight="bold")),
                ft.DataColumn(ft.Text("Team", weight="bold")),
                ft.DataColumn(ft.Text("Fastest Lap", weight="bold")),
                ft.DataColumn(ft.Text("Time", weight="bold")),
                ft.DataColumn(ft.Text("Points", weight="bold")),
            ]
        else:
            table.columns = [
                ft.DataColumn(ft.Text("Pos", weight="bold")),
                ft.DataColumn(ft.Text("Driver", weight="bold")),
                ft.DataColumn(ft.Text("Team", weight="bold")),
                ft.DataColumn(ft.Text("Quali Time", weight="bold")),
            ]
        #page.update()
        load_results(e)


    #-----------------------DECLARATIONS (MAIN)-----------------------------

    #dropdown declarations
    dropdown_race = ft.Dropdown(label="Select race",on_select=load_results)
    dropdown_season = ft.Dropdown(label="Select season",on_select=update_race_dropdown)
    segmented = ft.SegmentedButton(
        segments=[
            ft.Segment(value="race", label=ft.Text("Race")),
            ft.Segment(value="quali", label=ft.Text("Qualifying")),
        ],
        selected=["race"],
        on_change=switch_mode,
    )


    init_season_dropdown()

    #return view
    return ft.Column(
        [
            ft.Text("GP results", size=24, weight="bold"),
                ft.Row(
                [
                    segmented,
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
