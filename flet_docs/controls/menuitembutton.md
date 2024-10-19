---
title: MenuItemButton
sidebar_label: MenuItemButton
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

A button for use in a [MenuBar](/docs/controls/menubar) or on its own, that can be activated by click or keyboard
navigation.

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/menuitembutton)

### Basic Example

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    bg_container = ft.Ref[ft.Container]()

    def handle_color_click(e):
        color = e.control.content.value
        print(f"{color}.on_click")
        bg_container.current.content.value = f"{color} background color"
        bg_container.current.bgcolor = color.lower()
        page.update()

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("BgColors"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Blue"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.BLUE}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Green"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.GREEN}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Red"),
                        leading=ft.Icon(ft.icons.COLORIZE),
                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.colors.RED}),
                        on_click=handle_color_click,
                        on_hover=handle_on_hover,
                    )
                ]
            ),
        ]
    )

    page.add(
        ft.Row([menubar]),
        ft.Container(
            ref=bg_container,
            expand=True,
            bgcolor=ft.colors.SURFACE,
            content=ft.Text("Choose a bgcolor from the menu", style=ft.TextThemeStyle.HEADLINE_LARGE),
            alignment=ft.alignment.center,
        )
    )


ft.app(main)
```

  </TabItem>

</Tabs>

<img src="/img/docs/controls/menu-item-button/menu-item-button.gif" className="screenshot-20" />

## Properties

### `autofocus`

Whether this button should automatically request focus.

Defaults to `False`.

### `clip_behavior`

Whether to clip the content of this control or not.

Value is of type [`ClipBehavior`](/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.NONE`.

### `close_on_click`

Defines if the menu will be closed when the `MenuItemButton` is clicked.

Defaults to `True`.

### `content`

The child control to be displayed in the center of this button.

Typically this is the button's label, using a `Text` control.

### `focus_on_hover`

Determine if hovering can request focus.

Defaults to `True`.

### `leading`

An optional control to display before the `content`.

Typically an [`Icon`](/docs/controls/icon) control.

### `overflow_axis`

The direction in which the menu item expands.

If the menu item button is a descendent of `MenuBar`, then this property is ignored.

Value is of type [`Axis`](/docs/reference/types/axis).

### `semantic_label`

A string that describes the button's action to assistive technologies.

### `style`

Customizes this button's appearance.

Value is of type [`ButtonStyle`](/docs/reference/types/buttonstyle).

### `trailing`

An optional control to display after the `content`.

Typically an [`Icon`](/docs/controls/icon) control.

## Events

### `on_blur`

Fired when this button loses focus.

### `on_click`

Fired when the button is clicked.

### `on_focus`

Fired when the button receives focus.

### `on_hover`

Fired when the button is hovered.
