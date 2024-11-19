#### 3.2 Screen 2 Events

- **Use Icon Click**:
  - Placeholder for future functionality to use the selected list in the name picker view.
- **Save Icon Click**:
  - Save any edits made to the list items.
  - Provide visual feedback or a message indicating success.
- **Delete Icon Click**:
  - Show a confirmation dialog before deleting the list.
  - Remain on Screen 2 after deletion and clear the list details.
- **Search Input Change**:
  - Filter the items in the list based on the search query.
- **Input Field Changes**:
  - Update the state when any of the ID, Name, or Gender fields are modified.
- **Back Button Click**:
  - Navigate back to `ManageListsView` using the controller.
  - Handle any unsaved changes before navigating.
- **Header Icon Click**:
  - Ensure header icons have event handlers that are functional within `EditListView`.
  - Update the navigation logic to allow view changes from within `EditListView`.
- **Implement Two-Column Layout in Edit List View**: (2 columns separated by a thin line)
  - **Left Column**: Editing the currently selected list.
  - **Right Column**:
    - Search bar occupying half the screen.
    - Thin horizontal divider.
    - List of available lists (one list per line).

- **Fix Navigation Issues**:
  - **Back Button Functionality**:
    - Ensure the back button navigates back to the manage lists view.
    - Handle any unsaved changes before navigating.
  - **Header Icon Navigation**:
    - Add event handlers to the user account icon in the header to allow view changes.
    - Ensure clicking the icon successfully transitions to the user account view.
    - The left sidebar must be visible at all times (make the edit list view display the same as other views: left sidebar on the left, on the right is header on top and the view content area below it)

### 4. Logging

- **Setup Logging**:
  - Configure the logging module to write logs to a file (e.g., `app.log`).
  - Set an appropriate logging level (e.g., `logging.DEBUG`).
- **Add Logging Statements**:
  - **View Changes**: Log when the user navigates between screens.
  - **Button Clicks**: Log button presses with details (e.g., which list was edited or deleted).
  - **UI Updates**: Log significant UI updates or state changes.
- **Use Different Log Levels**:
  - **DEBUG**: Detailed information for diagnosing issues.
  - **INFO**: Confirmation of normal operations.
  - **WARNING**: Unexpected events that are handled.
  - **ERROR**: Serious problems that prevent functionality.

### 5. Testing

- **Functionality Tests**:
  - Verify that search filters work correctly on both screens.
  - Ensure that editing and saving list items function as expected.
  - Test delete actions to confirm that confirmation dialogs appear and actions are executed.
- **UI Tests**:
  - Check that the layout matches the design specifications.
  - Ensure that the UI is responsive and controls are properly aligned.
- **Logging Tests**:
  - Review the log file to ensure that all key actions are logged appropriately.
  - Confirm that the log levels are used correctly and that the log is not too verbose.

## Summary of Changes to Files

### `manage_lists_view.py`

- **Create New Class**: `ManageListsView` handling both Screen 1 and Screen 2.
- **Implement Methods**:
  - `build()`: Determine which screen to display based on the current state.
  - `build_screen_1()`: Build the UI for Screen 1 (List Overview).
  - `build_screen_2()`: Build the UI for Screen 2 (List Details).
- **Event Handlers**:
  - `on_search_change()`: Handle dynamic filtering in search bars.
  - `on_edit_click()`: Transition to Screen 2 with the selected list.
  - `on_delete_click()`: Display confirmation dialog and handle deletion.
  - `on_save_click()`: Save edits made to a list.
  - `on_use_click()`: Placeholder for future functionality.
  - `on_back_click()`: Navigate back to `ManageListsView` and handle unsaved changes.
  - `on_header_icon_click()`: Handle navigation from header icons.
- **Update Grid Layout**:
  - Changed `runs_count` from `2` to `3` in the `GridView` to display three lists per row.
- **Remove Placeholder Lists**:
  - Removed the placeholder list items generation.
  - Implemented loading of lists from `saved_lists.json` via the controller.
- **Add Vertical Divider in Screen 2**:
  - Ensured a `VerticalDivider` is present between the two halves of Screen 2 for better distinction.
