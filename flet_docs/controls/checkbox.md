---
title: Checkbox
sidebar_label: Checkbox
---

Checkbox allows to select one or more items from a group, or switch between two mutually exclusive options (checked or unchecked, on or off).

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/checkbox)

### Basic checkboxes

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft

def main(page):
    def button_clicked(e):
        t.value = (
            f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
        )
        page.update()

    t = ft.Text()
    c1 = ft.Checkbox(label="Unchecked by default checkbox", value=False)
    c2 = ft.Checkbox(label="Undefined by default tristate checkbox", tristate=True)
    c3 = ft.Checkbox(label="Checked by default checkbox", value=True)
    c4 = ft.Checkbox(label="Disabled checkbox", disabled=True)
    c5 = ft.Checkbox(
        label="Checkbox with rendered label_position='left'", label_position=ft.LabelPosition.LEFT
    )
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(c1, c2, c3, c4, c5, b, t)

ft.app(main)
```
  </TabItem>
</Tabs>

<img src="/img/docs/controls/checkbox/basic-checkbox.gif" className="screenshot-40" />

### Checkbox with `on_change` event

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft

def main(page):
  def checkbox_changed(e):
    t.value = f"Checkbox value changed to {c.value}" 
    t.update()

  c = ft.Checkbox(label="Checkbox with 'change' event", on_change=checkbox_changed)
  t = ft.Text()

  page.add(c, t)

ft.app(main)
```
  </TabItem>
</Tabs>

<img src="/img/docs/controls/checkbox/checkbox-with-change-event.gif" className="screenshot-40" />

## Properties

### `active_color`

The [color](/docs/reference/colors) to use when this checkbox is checked.

### `adaptive`

If the value is `True`, an adaptive Checkbox is created based on whether the target platform is iOS/macOS.

On iOS and macOS, a [`CupertinoCheckbox`](/docs/controls/cupertinocheckbox) is created, which has matching functionality and presentation as `Checkbox`, and the graphics as expected on iOS. On other platforms, a Material Checkbox is created.

See the example of usage [here](/docs/controls/cupertinocheckbox#cupertinocheckbox-and-adaptive-checkbox-example).

Defaults to `False`.

### `autofocus`

True if the control will be selected as the initial focus. If there is more than one control on a page with autofocus set, then the first one added to the page will get focus.

### `border`

The color and width of the checkbox's border to be rendered when the checkbox's `value` is `False`.

### `check_color`

The [color](/docs/reference/colors) to use for the check icon when this checkbox is checked.

### `fill_color`

The [color](/docs/reference/colors) that fills the checkbox in
various [`ControlState`](/docs/reference/types/controlstate) states.

### `hover_color`

The [color](/docs/reference/colors) to use when this checkbox is hovered.

### `is_error`

Whether this checkbox wants to show an error state. When `True` this checkbox will have a different default container color and check color. Defaults to `False`.

### `label`

The clickable label to display on the right of a checkbox.

### `label_style`

The label's style. An instance of type [`TextStyle`](/docs/reference/types/textstyle).

### `label_position`

Defines on which side of the checkbox the `label` should be shown.

Value is of type [`LabelPosition`](/docs/reference/types/labelposition) and defaults to `LabelPosition.RIGHT`.

### `mouse_cursor`

The cursor to be displayed when a mouse pointer enters or is hovering over this control.

Value is of type [`MouseCursor`](/docs/reference/types/mousecursor).

### `overlay_color`

The [color](/docs/reference/colors) of the checkbox's overlay in
various [`ControlState`](/docs/reference/types/controlstate) states.

This property supports the following `ControlState` values: `PRESSED`, `SELECTED`, `HOVERED` and `FOCUSED`.

### `semantics_label`

The semantic label for the checkbox that is not shown in the UI, but will be announced by screen readers in accessibility modes (e.g TalkBack/VoiceOver).

### `shape`

The shape of the checkbox. The value is an instance of [`OutlinedBorder`](/docs/reference/types/outlinedborder) class.

Defaults to `RoundedRectangleBorder(radius=2)`.

### `splash_radius`

The radius of the circular Material ink response (ripple) in logical pixels.

Defaults to `20.0`.

### `tristate`

If `True` the checkboxes value can be `True`, `False`, or `None`.

Checkbox displays a dash when its value is `None`.

### `value`

Current value of the checkbox.

## Events

### `on_blur`

Fires when the control has lost focus.

### `on_change`

Fires when the state of the Checkbox is changed.

### `on_focus`

Fires when the control has received focus.
