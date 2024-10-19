---
title: CupertinoTimerPicker
sidebar_label: CupertinoTimerPicker
---

A countdown timer picker in iOS style.

To open this control, simply call the [`page.open()`](/docs/controls/page#opencontrol) helper-method.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/cupertinotimerpicker)

### Basic Example

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import time
import flet as ft


def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    timer_picker_value_ref = ft.Ref[ft.Text]()

    def handle_timer_picker_change(e):
        # e.data is the selected time in seconds
        timer_picker_value_ref.current.value = time.strftime("%H:%M:%S", time.gmtime(int(e.data)))
        page.update()

    cupertino_timer_picker = ft.CupertinoTimerPicker(
        value=3600,
        second_interval=10,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
    )

    page.add(
        ft.Row(
            tight=True,
            controls=[
                ft.Text("TimerPicker Value:", size=23),
                ft.CupertinoButton(
                    content=ft.Text(
                        ref=timer_picker_value_ref,
                        value="00:01:10",
                        size=23,
                        color=ft.cupertino_colors.DESTRUCTIVE_RED,
                    ),
                    on_click=lambda e: page.open(
                        ft.CupertinoBottomSheet(
                            cupertino_timer_picker,
                            height=216,
                            padding=ft.padding.only(top=6),
                        )
                    ),
                ),
            ],
        ),
    )


ft.app(main)
```
  </TabItem>
</Tabs>

<img src="/img/docs/controls/cupertino-timer-picker/basic-cupertino-timer-picker.gif" className="screenshot-50" />

## Properties

### `alignment`

Defines how the timer picker should be positioned within its parent. 

Value is of type [`Alignment`](/docs/reference/types/alignment) and defaults to `alignment.center`.

### `bgcolor`

The background [color](/docs/reference/colors) of the timer picker.

### `mode`

The mode of the timer picker. Value is of
type [`CupertinoTimerPickerMode`](/docs/reference/types/cupertinotimerpickermode) and defaults
to `CupertinoTimerPickerMode.HOUR_MINUTE_SECOND`.

### `item_extent`

The uniform height of all children.

Defaults to `32`.

### `second_interval`

The granularity of the second spinner. Must be a positive integer factor of 60.

Defaults to `1`.

### `minute_interval`

The granularity of the minute spinner. Must be a positive integer factor of 60.

Defaults to `1`.

### `value`

The initial duration in seconds of the countdown timer.

Defaults to `0`.

## Events

### `on_change`

Fires when the timer duration changes.