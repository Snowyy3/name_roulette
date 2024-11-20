# Implementation Plan

This plan outlines the steps to integrate `ManageListsView` and `EditListView` into the main application, ensuring that the left sidebar and header are always present, and that user-specific list management is properly implemented.

## 1. Update `views.py`

- **Add Enum Values**:
    - Add `MANAGE_LISTS` and `EDIT_LIST` to the `View` enum.

## 2. Modify `MainView` (`main_view.py`)

- **View Handling**:
    - Update `handle_view_change()` to handle the new views `MANAGE_LISTS` and `EDIT_LIST`.
    - Ensure the content area displays the appropriate view based on the current selection.
    - Keep the left sidebar and header visible at all times.

- **Add `ManageListsView` and `EditListView`**:
    - Instantiate `ManageListsView` and `EditListView` within `MainView`.
    - Pass necessary controllers and state to these views.

- **Update Navigation Logic**:
    - Implement methods in the controller to navigate between `ManageListsView` and `EditListView`.
    - Ensure back navigation and header icons function correctly.

## 3. Implement 'Use List' Button Functionality in `EditListView`

- **Add Dropdown Menu**:
    - Modify the 'Use List' button to display a dropdown with options:
        - "Use in Name Picker"
        - "Use in Group Former"
    - On selection, navigate to the chosen view with the selected list.

- **Populate Input Fields**:
    - Ensure that the selected list from `EditListView` is pre-loaded into the input fields of the destination view.

## 4. Implement Persistent Search State and Autocomplete

- **Persist Search State**:
    - Store the search query in a variable that persists between view transitions.
    - Apply the search filter when returning to the view.

- **Use Autocomplete in Search Fields**:
    - Replace existing `TextField` search inputs with `Autocomplete` components if possible.
    - If icons cannot be added to the autocomplete field, retain the current implementation.

## 5. Handle Unsaved Changes in `EditListView`

- **Detect Unsaved Changes**:
    - Implement a flag `has_unsaved_changes` to track edits.
    - Set the flag to `True` whenever the list name or items are modified.

- **Show `AlertDialog` on Navigation**:
    - Before navigating away, check if `has_unsaved_changes` is `True`.
    - Show an `AlertDialog` with options:
        - Cancel: Close the dialog and stay on the current view.
        - Discard: Discard changes and navigate away.
        - Save: Save changes and navigate away.

## 6. Update `ListController` for User-Specific Lists

- **Modify Data Structure**:
    - Change `ListController` to load and save lists based on the authenticated user.
    - Use `users.json` for authentication and `saved_lists.json` for storing lists.

- **Handle Authenticated Users**:
    - When a user is logged in, load their lists from `saved_lists.json`.
    - Save changes to their specific list entries.

- **Handle Unauthorized Users**:
    - Allow unauthorized users to create, edit, and delete lists.
    - Store these lists in a temporary variable or a temp file.
    - Ensure that these lists are not persisted after the application closes.

- **Implement Missing Methods**:
    - Ensure that methods like `set_active_list`, `navigate_to_name_picker`, and `navigate_to_group_former` are implemented in the controller to support the new functionality.

## 7. Adjust Data Persistence in `saved_lists.json`

- **Align with `users.json` Structure**:
    - Update `saved_lists.json` to use usernames as keys, matching the `users.json` structure.

## 8. UI Adjustments

- **Consistent `AppBar` and Sidebar**:
    - Modify `ManageListsView` and `EditListView` to use the common `AppBar` and sidebar.
    - Remove any redundant headers or back buttons if they duplicate the `AppBar` functionality.

- **Place Additional Buttons Below `AppBar`**:
    - Place any view-specific buttons (e.g., 'Use List', 'Save') below the header in the view's content area.

- **Implement Two-Column Layout in `EditListView`**:
    - **Left Column**:
        - Contains fields to edit the currently selected list.
        - Includes list name and items.
    - **Right Column**:
        - Contains a search bar at the top.
        - Below the search bar, display a list of available lists, one list per line.
    - Use a `Row` with two `Column` widgets to achieve the layout.

## 9. Enhance Navigation and Event Handling

- **Navigation Methods in Controller**:
    - Implement methods like `navigate_to_manage_lists` and `navigate_to_edit_list` in the main controller.

- **Update Event Handlers**:
    - Ensure all buttons and icons have proper event handlers to navigate between views.
    - Update the `on_click` events in the UI components accordingly.

## 10. Testing

- **Functionality Tests**:
    - Test navigation between all views, ensuring the left sidebar and header are always visible.
    - Verify that the 'Use List' functionality works as intended and pre-populates data.

- **Unsaved Changes**:
    - Test the unsaved changes dialog by editing a list and attempting to navigate away.
    - Verify that each button in the dialog performs the correct action.

- **User Authentication Tests**:
    - Log in as different users and confirm that only their lists are visible and editable.
    - Check that unauthorized users cannot access other users' lists.

- **Temporary Lists for Unauthorized Users**:
    - Create lists as an unauthorized user.
    - Confirm that these lists are not saved after closing the application.

## 11. Code Cleanup and Documentation

- **Refactor Code**:
    - Review and refactor code in `main_view.py`, `manage_lists_view.py`, and `edit_list_view.py` to reduce redundancy.
    - Remove any obsolete or redundant code segments.

- **Add Comments and Docstrings**:
    - Ensure that all new methods and classes are properly documented.
    - Update existing comments to reflect code changes.

- **Follow PEP 8 Guidelines**:
    - Check code formatting and style to comply with PEP 8 standards.

## 12. Logging Enhancements

- **Consistent Logging**:
    - Add logging statements to new functionalities to assist in debugging.
    - Ensure all exceptions are properly caught and logged.

- **Logging Levels**:
    - Use appropriate logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) throughout the code.

## 13. Future Considerations

- **Autocomplete Icons**:
    - Research the possibility of adding icons to autocomplete components for future UI enhancements.

- **Two-Column Layout Enhancements**:
    - Plan for further improvements to the two-column layout in `EditListView` based on user feedback.
