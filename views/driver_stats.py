import flet as ft
from api import fetch_results, fetch_quali_results,get_driver_list,get_driver_stats_quali,get_driver_stats_race



def driver_stats_view(page: ft.Page):

    #-------------------DECLARATIONS----------------------

    wins_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    podiums_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    avg_finish_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    pole_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    avg_quali_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    sprint_wins_text = ft.Text("0", weight=ft.FontWeight.BOLD)
    sprint_poles_text = ft.Text("0", weight=ft.FontWeight.BOLD)

    def stat_row(label: str, value_control):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(label, weight=ft.FontWeight.W_500),
                value_control,
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

    def show_driver_stats():
        race_stats = get_driver_stats_race(int(dropdown_season.value), str(dropdown_driver.value))
        #quali_stats = get_driver_stats_quali(int(dropdown_season.value), str(dropdown_driver.value))
        wins = 0
        podiums = 0
        avg_position = []
        quali_wins = 0
        avg_quali = []

        for race in race_stats:
            avg_position.append(race['position'])
            if race['position'] == 1:
                wins+=1
            if race['position'] >= 1 and race['position'] <=3:
                podiums+=1
        
        #for quali in quali_stats:
        #    avg_quali.append(quali['position'])
        #    if quali['position'] == 1:
        #        quali_wins +=1

        wins_text.value = str(wins)
        podiums_text.value = str(podiums)
        avg_finish_text.value = str(sum(avg_position)/len(avg_position))
        #pole_text.value = str(quali_wins)
        #avg_quali_text.value = str(sum(avg_quali)/len(avg_quali))

        page.update()


    dropdown_season = ft.Dropdown(label="Select season",on_select=update_driver_list)
    dropdown_driver = ft.Dropdown(label="Select driver",on_select=show_driver_stats)






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
            stat_row("Wins", wins_text),
            stat_row("Podiums", podiums_text),
            stat_row("Average Finish Position", avg_finish_text),
            #stat_row("Pole Positions", pole_text),
            #stat_row("Average Qualifying", avg_quali_text),
           ],
 
       )
