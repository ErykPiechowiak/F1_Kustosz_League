import flet as ft
from views.championship import championship_view
from views.race_results import race_results_view


def main(page: ft.Page):
    page.title = "F1 Kustosz League"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    content = ft.Column(expand=True)

    def show_championship(e=None):
        content.controls = [championship_view(page)]
        page.update()

    def show_race_results(e=None):
        content.controls = [race_results_view(page)]
        page.update()

    page.add(
        ft.Row(
            [
                #ft.Text("F1 Kustosz League", size=28, weight="bold"),
                ft.Row(
                    [
                        ft.Button("Championship", on_click=show_championship),
                        ft.Button("GP results", on_click=show_race_results),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        ft.Divider(),
        content,
    )

    show_championship()


ft.run(main)
