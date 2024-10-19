---
title: CupertinoFilledButton
sidebar_label: CupertinoFilledButton
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

An iOS-style button with filled with background color.

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/cupertinofilledbutton)

### Basic Example

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilled"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clicked!"),
        ),
    )

ft.app(main)
```
  </TabItem>

</Tabs>

<img src="/img/docs/controls/cupertino-filled-button/cupertino-filled-button.png" className="screenshot-20" />

## Properties

### `disabled_color`

The background [color](/docs/reference/colors) of the button when it is disabled.

### `content`

A Control representing custom button content.

### `icon`

Icon shown in the button.

### `icon_color`

Icon [color](/docs/reference/colors).

### `min_size`

The minimum size of the button.

Defaults to `44.0`.

### `opacity_on_click`

Defines the opacity of the button when it is clicked.

Defaults to `0.4`. The button will have an opacity of `1.0` when it is not pressed.

### `padding`

The amount of space to surround the `content` control inside the bounds of the button.

### `text`

The text displayed on a button.

### `tooltip`

The text displayed when hovering the mouse over the button.

### `url`

The URL to open when the button is clicked. If registered, `on_click` event is fired after that.

### `url_target`

Where to open URL in the web mode.

Value is of type [`UrlTarget`](/docs/reference/types/urltarget) and defaults to `UrlTarget.BLANK`.

## Events

### `on_click`

Fires when a user clicks the button.
