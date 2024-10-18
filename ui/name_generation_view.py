import flet as ft


class NameGenerationView(ft.UserControl):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def build(self):
        # Left half: Input field
        self.name_input = ft.TextField(
            label="Enter names (one per line)",
            multiline=True,
            min_lines=10,
            max_lines=20,
            expand=True
        )

        left_column = ft.Column([
            ft.Text("Name Input", style=ft.TextThemeStyle.TITLE_MEDIUM),
            self.name_input
        ], expand=True)

        # Right half: Filters and Generate button
        self.gender_filter = ft.Dropdown(
            label="Filter by Gender",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("Male"),
                ft.dropdown.Option("Female"),
            ],
            value="All",
        )

        self.generate_button = ft.ElevatedButton(
            text="Generate Random Names",
            on_click=self.generate_names
        )

        self.result_list = ft.ListView(expand=1, spacing=10, padding=20)

        right_column = ft.Column([
            ft.Text("Filters", style=ft.TextThemeStyle.TITLE_MEDIUM),
            self.gender_filter,
            self.generate_button,
            ft.Divider(),
            ft.Text("Generated Names:"),
            self.result_list
        ], expand=True)

        # Main layout
        main_row = ft.Row([
            left_column,
            ft.VerticalDivider(width=1),
            right_column
        ], expand=True)

        self.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Name Generation", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                    main_row
                ]),
                expand=True,
                padding=10
            )
        )

    def generate_names(self, e):
        if self.name_input.value:
            names = self.name_input.value.split("\n")
            gender_filter = self.gender_filter.value
            randomized_names = self.controller.generate_random_names(names, gender_filter)

            self.result_list.controls.clear()
            for name in randomized_names:
                self.result_list.controls.append(ft.Text(name))
        else:
            # Handle the case when no names are entered
            self.result_list.controls.clear()
            self.result_list.controls.append(ft.Text("No names entered"))
        
        self.result_list.update()
