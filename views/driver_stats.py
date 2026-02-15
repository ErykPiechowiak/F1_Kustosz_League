import flet as ft
from api import fetch_results, fetch_quali_results,get_driver_list,get_driver_stats_quali,get_driver_stats_race



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

    def init_dropdown_season():
        #results = fetch_results()
        seasons = ["1","2"]
        dropdown_season.options = [ft.dropdown.Option(r) for r in seasons]
        #drivers = get_driver_list(1)
        #print(drivers)
        #dropdown_driver.options = [ft.dropdown.Option(r) for r in drivers]
        #page.update()


    def update_driver_list():
        drivers = get_driver_list(dropdown_season.value)
        dropdown_driver.options = [ft.dropdown.Option(r) for r in drivers]
        page.update()

    dropdown_season = ft.Dropdown(label="Select season",on_select=update_driver_list)
    dropdown_driver = ft.Dropdown(label="Select driver",on_select=temp)






    init_dropdown_season()

    #return view
    return ft.Column(
           controls=[
                ft.Row(
                [
                    dropdown_season,
                    dropdown_driver,
                ],
                spacing = 100
                ),
               stat_row("Wins","OK"),#, driver_stats["points"]),
               stat_row("Podiums","OK"),#, driver_stats["wins"]),
               stat_row("Average Finish Position","OK"),#, driver_stats["podiums"]),
               stat_row("Pole Positions","OK"),#, driver_stats["poles"]),
               stat_row("Average Qualifying ","OK"),#, driver_stats["avg_position"]),
               stat_row("Sprint Wins ","OK"),#, driver_stats["avg_position"]),
               stat_row("Sprint Pole Positions ","OK"),#, driver_stats["avg_position"]),

           ],
 
       )
