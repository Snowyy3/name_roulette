- Use filled (tonal) buttons for confirmation dialogues (such as make the Cancel button of Delete cf diag filled with red/blue, the Confirm button remains as is)
- Might change color of icons in existing ElevatedButtons
- Use dropdown with label and hint for lists selection
- Use Switch for toggle Light/Dark theme
- Change layout of header and sidebar

```log
future: <Future finished exception=AttributeError("'MainController' object has no attribute 'form_groups'")>
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\concurrent\futures\thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\page.py", line 944, in wrapper
    handler(*args)
  File "x:\Programming\Python\Projects\Name Roulette\ui\group_former_view.py", line 419, in handle_randomize_click
    self.form_groups(e)  # Call the original logic
    ^^^^^^^^^^^^^^^^^^^
  File "x:\Programming\Python\Projects\Name Roulette\ui\group_former_view.py", line 673, in form_groups
    generated_groups = self.controller.form_groups(names, group_size, group_num)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'MainController' object has no attribute 'form_groups'
```

```log
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\concurrent\futures\thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\page.py", line 944, in wrapper
    handler(*args)
  File "X:\Programming\Python\Projects\Name Roulette\ui\login_view.py", line 163, in handle_guest_login
    self.on_login(None, None)  # Pass None to indicate guest login
    ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "X:\Programming\Python\Projects\Name Roulette\ui\main_view.py", line 245, in handle_login
    self.handle_view_change(target_view)
  File "X:\Programming\Python\Projects\Name Roulette\ui\main_view.py", line 161, in handle_view_change
    self._update_content_area(view, view_instance)
  File "X:\Programming\Python\Projects\Name Roulette\ui\main_view.py", line 198, in _update_content_area
    self.content_area.update()
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\control.py", line 310, in update
    self.__page.update(self)
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\page.py", line 721, in update
    r = self.__update(*controls)
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\page.py", line 833, in __update
    commands, added_controls, removed_controls = self.__prepare_update(*controls)
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\page.py", line 849, in __prepare_update
    control.build_update_commands(
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\control.py", line 467, in build_update_commands
    ctrl.build_update_commands(
  File "X:\Programming\Python\Projects\Name Roulette\.env-name\Lib\site-packages\flet_core\control.py", line 448, in build_update_commands
    innerCmds = ctrl._build_add_commands(
                ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '_build_add_commands'
```



- Group former view:
  + fix drag interval bug (cái này tạm bỏ qua, fix sau)
  + random (no gender) doesn't work


- # TODO: Major refactor of controllers and related logics (aside from login, sign up, user auth)
