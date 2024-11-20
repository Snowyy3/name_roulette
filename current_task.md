**Objective:**
Refactor these attached files (everything related to group former) to improve code maintainability, readability, and adherence to the MVC architecture. The refactoring should:

1. Break down large methods into smaller, more manageable methods.
2. Identify and move methods that belong in the model.
3. Identify and move methods that belong in the controller.
4. Ensure correct usage of method names and proper delegation of responsibilities.
5. Mitigate mistakes such as incorrect method calls and improper placements of logic.

**Instructions:**

1. **Refactor Large Methods:**
  - Identify large methods in the 3 files, especially `GroupFormerView` and refactor them into smaller, focused methods.
  - Ensure each method has a single responsibility.

2. **Determine Methods for the Model:**
  - Identify methods that involve data processing, validation, or business logic.
  - Move these methods to the appropriate model class.

3. **Determine Methods for the Controller:**
  - Identify methods that involve coordinating between the view and the model.
  - Move these methods to the appropriate controller class.

4. **Ensure Correct Method Usage:**
  - Review the refactored code to ensure methods are called from the correct places.
  - Verify that the view only handles UI updates and event delegation.
  - Ensure the controller mediates between the view and the model correctly.

5. **Thorough Review:**
  - Perform a step-by-step review of the refactored code.
  - Check for any incorrect method names, misplaced logic, or broken functionality.
  - Ensure the refactored code works as expected.
