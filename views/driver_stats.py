import flet as ft
from api import fetch_results, fetch_quali_results,get_driver_list



def driver_stats_view(page: ft.Page):

    def stat_row(label: str, value: str):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, weight=ft.FontWeight.W_500),
                ft.Text(str(value), weight=ft.FontWeight.BOLD),
            ],
        )

    
    def temp():
        print("nice")


    #-----------------------DROPDOWN-------------------------
    dropdown_season = ft.Dropdown(label="Select season",on_select=temp)
    dropdown_driver = ft.Dropdown(label="Select season",on_select=temp)

    def init_dropdowns():
        #results = fetch_results()
        seasons = ["1","2"]
        dropdown_season.options = [ft.dropdown.Option(r) for r in seasons]
        drivers = get_driver_list()
        print(drivers)
        dropdown_driver.options = [ft.dropdown.Option(r) for r in drivers]
        page.update()


    init_dropdowns()

    #return view
    return ft.Column(
           spacing=10,
           controls=[
               stat_row("Punkty","OK"),#, driver_stats["points"]),
               stat_row("Wygrane","OK"),#, driver_stats["wins"]),
               stat_row("Podia","OK"),#, driver_stats["podiums"]),
               stat_row("Pole position","OK"),#, driver_stats["poles"]),
               stat_row("Średnia pozycja","OK"),#, driver_stats["avg_position"]),
           ]
       )
