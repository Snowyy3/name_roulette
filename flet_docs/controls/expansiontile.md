---
title: ExpansionTile
sidebar_label: ExpansionTile
---

A single-line ListTile with an expansion arrow icon that expands or collapses the tile to reveal or hide its children.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansiontile)

<img src="/img/docs/controls/expansion-tile/expansion-tile.png" className="screenshot-50"/>

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft


def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0

    def handle_expansion_tile_change(e):
        page.open(
            ft.SnackBar(
                ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"),
                duration=1000,
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE
                else ft.icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    page.add(
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 1"),
            subtitle=ft.Text("Trailing expansion arrow icon"),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.colors.RED,
            text_color=ft.colors.RED,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 1"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 2"),
            subtitle=ft.Text("Custom expansion arrow icon"),
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
            collapsed_text_color=ft.colors.GREEN,
            text_color=ft.colors.GREEN,
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 2"))],
        ),
        ft.ExpansionTile(
            title=ft.Text("ExpansionTile 3"),
            subtitle=ft.Text("Leading expansion arrow icon"),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=True,
            collapsed_text_color=ft.colors.BLUE,
            text_color=ft.colors.BLUE,
            controls=[
                ft.ListTile(title=ft.Text("This is sub-tile number 3")),
                ft.ListTile(title=ft.Text("This is sub-tile number 4")),
                ft.ListTile(title=ft.Text("This is sub-tile number 5")),
            ],
        ),
    )


ft.app(main)
```
  </TabItem>
</Tabs>

## Properties

### `affinity`

Typically used to force the expansion arrow icon to the tile's `leading` or `trailing` edge.

Value is of type [`TileAffinity`](/docs/reference/types/tileaffinity) and defaults to `TileAffinity.PLATFORM`.

### `bgcolor`

The  [color](/docs/reference/colors) to display behind the sublist when expanded.

### `controls`

The controls to be displayed when the tile expands.

Typically a list of [`ListTile`](/docs/controls/listtile) controls.

### `controls_padding`

Defines the padding around the `controls`.

Padding value is an instance of [`Padding`](/docs/reference/types/padding).

### `clip_behavior`

The content will be clipped (or not) according to this option.

Value is of type [`ClipBehavior`](/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.NONE`.

### `collapsed_bgcolor`

Defines the background [color](/docs/reference/colors) of tile when the sublist is collapsed.

### `collapsed_icon_color`

The icon [color](/docs/reference/colors) of tile's expansion arrow icon when the sublist is collapsed.

### `collapsed_shape`

The tile's border shape when the sublist is collapsed. The value is an instance
of [`OutlinedBorder`](/docs/reference/types/outlinedborder).

### `collapsed_text_color`

The [color](/docs/reference/colors) of the tile's titles when the sublist is collapsed.

### `dense`

Whether this list tile is part of a vertically dense list. Dense list tiles default to a smaller height.

It is not recommended to set this property to `True` when in Material3.

Defaults to `False`.

### `enable_feedback`

Whether detected gestures should provide acoustic and/or haptic feedback. For example, on Android a tap will produce a clicking sound and a long-press will produce a short vibration, when feedback is enabled.

Defaults to `True`.

### `expanded_alignment`

Defines the alignment of children, which are arranged in a column when the tile is expanded.

Value is of type [`Alignment`](/docs/reference/types/alignment).

### `expanded_cross_axis_alignment`

Defines the alignment of each child control within `controls` when the tile is expanded.

Value is of type [`CrossAxisAlignment`](/docs/reference/types/crossaxisalignment) and defaults
to `CrossAxisAlignment.CENTER`.

### `icon_color`

The icon [color](/docs/reference/colors) of tile's expansion arrow icon when the sublist is expanded.

### `initially_expanded`

A boolean value which defines whether the tile is initially expanded or collapsed.

Defaults to `False`.

### `leading`

A `Control` to display before the title.

### `maintain_state`

A boolean value which defines whether the state of the `controls` is maintained when the tile expands and collapses.

Defaults to `False`.

### `min_tile_height`

The minimum height of the tile.

### `shape`

The tile's border shape when the sublist is expanded.

Value is of type [`OutlinedBorder`](/docs/reference/types/outlinedborder).

### `show_trailing_icon`

Whether to show the trailing icon (be it the default icon or the custom `trailing`, if specified and visible).

Defaults to `True`.

### `subtitle`

Additional content displayed below the title.

Typically a [`Text`](/docs/controls/text) control.

### `text_color`

The [color](/docs/reference/colors) of the tile's titles when the sublist is expanded.

### `tile_padding`

Defines the tile's padding. Default value is `padding.symmetric(horizontal=16.0)`.

Padding value is an instance of [`Padding`](/docs/reference/types/padding) class.

### `title`

A `Control` to display as primary content of the tile.

Typically a [`Text`](/docs/controls/text) control.

### `trailing`

A `Control` to display after the title.

Typically an [`Icon`](/docs/controls/icon) control.

### `visual_density`

Defines how compact the control's layout will be.

Value is of type [`ThemeVisualDensity`](/docs/reference/types/themevisualdensity).

## Events

### `on_change`

Fires when a user clicks or taps the list tile.

### `on_long_press`

Fires when the user long-presses on this list tile.