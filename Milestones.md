## **Name Roulette: Project Milestones**

### **Group 2** - List of members:

| **Index** | **Student ID** | **Full name** |
|:---:|:---:|:---|
| 0 | 11230522 | Thành Uyển Dung |
| 1 | 11230512 | Nguyễn Thị Mai Anh |
| 2 | 11230530 | Nguyễn Phương Đông |
| 3 | 11230538 | Nguyễn Hoàng |
| 4 | 11230553 | Hàn Chí Kiên |
| 5 | 11230574 | Nguyễn Phú Nam |
| 6 | 11230552 | Đỗ Hữu Kiên |



### **Preliminary Plan**

**A. Main Modules:**

1.  **Data Management Module (`data_manager.py`):**
    -   Handles loading, parsing, and storing the name dataset (e.g., from CSV, JSON).
    -   Provides functions for accessing and filtering the dataset based on various criteria (gender, attributes).
    -   **Added Functionality:**
        -   Implements saving and loading user-defined class lists (e.g., using pickle, JSON).

2.  **Randomization Engine Module (`randomizer.py`):**
    -   Implements core algorithms for generating random names and groups.
    -   Handles gender balancing and representative picking logic.

3.  **User Interface (UI) Module (`ui.py`):**
    -   Provides a user-friendly interface for interacting with the application.
    -   Allows users to input parameters, trigger name/group generation, and view results.
    -   **Added Functionality:**
        -   Includes features for pasting and saving class lists.

**B. Core Features:**

1.  **Basic Name Generation:**
    -   Generate a specified number of random names from the dataset.

2.  **Gender Filtering:**
    -   Filter names based on gender (male, female, or both).
    -   Control the number or percentage of males/females in the generated list.

3.  **Basic Group Generation:**
    -   Create a specified number of groups with a specified number of members per group.

4.  **Gender Balancing in Groups:**
    -   Control the gender distribution within each generated group.

5.  **Representative Picking:**
    -   Allow users to pre-assign specific individuals to certain groups, with the remaining members randomly assigned.

6.  **Custom Class Lists:**
    -   Allow users to paste and save lists of students for specific classes.
    -   Use these custom lists for name generation and group formation.

**C. Development Approach:**

1.  **Modular Design:** Develop the application using a modular approach, with clear separation of concerns between modules. This promotes code reusability and maintainability.

2.  **Iterative Development:** Follow an iterative development process, starting with core features and gradually adding more advanced functionalities based on user feedback and project scope.

3.  **Testing and Refinement:** Emphasize thorough testing throughout the development process, including unit testing, integration testing, and user acceptance testing.

**D. Suggested File Structure:**

```
name_roulette/
├── data_manager.py
├── randomizer.py
├── ui.py
└── data/ 
    └── class_lists/  # Store user-defined class lists here (e.g., as JSON files)
```

**E. Major Milestones:**

1.  **Core Functionality Development:**
    -   **Name Dataset Management:**
        -   Decide on the format and source of the name dataset (e.g., CSV, JSON).
        -   Implement functions in `data_manager.py` to load, parse, and store the dataset.
        -   Implement functions to save and load custom class lists.
    -   **Random Name Generation:**
        -   Develop algorithms in `randomizer.py` for generating random names based on user-specified criteria.
    -   **Group Generation:**
        -   Implement algorithms in `randomizer.py` for creating balanced groups.

2.  **User Interface (UI) Development:**
    -   **UI Framework Selection:** Choose a suitable Python UI framework (e.g., Tkinter, PyQt).
    -   **UI Design and Implementation:** Design and implement the UI in `ui.py`, including:
        -   Input fields for user parameters.
        -   Output display for generated names and groups.
        -   Features for pasting and saving class lists.
        -   Intuitive controls and navigation.

3.  **Testing and Refinement:**
    -   **Unit Testing:** Develop unit tests to ensure the correctness of core functionalities in `data_manager.py` and `randomizer.py`.
    -   **Integration Testing:** Test the integration between the UI and core functionalities.
    -   **User Acceptance Testing (UAT):** Gather feedback from potential users and refine the application.

4.  **Documentation and Deployment:**
    -   **User Manual:** Create a user manual or help documentation.
    -   **Code Documentation:** Document the code using comments and docstrings.
    -   **Deployment:** Explore options for deploying the application (e.g., creating an executable).


### **Python Libraries** *(options, not 100% required)*

-   **Data Manipulation:**
    -   **Pandas**: For efficient data loading, manipulation, and filtering.
    -   **Pickle/JSON**: For saving and loading custom class lists.
-   **UI Development:**
    -   **Tkinter**: A standard Python UI framework (beginner-friendly).
    -   **PyQt**: A more advanced and feature-rich UI framework.
-   **Randomization:**
    -   `random`: Python's built-in module for random number generation.
    -   If possible, we can opt for self-made randomization module instead of having to rely on external dependencies *(might not be as 'random' as mature solutions)*
-   **Other Potential Libraries:**
    -   **NumPy**: For numerical operations (if needed for attribute-based filtering).


## **B. Comprehensive Task List**

**(Tasks are grouped by module and feature)**

**1. Data Management Module (`data_manager.py`):**

-   **Name Dataset:**
    -   Research and select a suitable name dataset source.
    -   Implement data loading and parsing functions.
    -   Design and implement data storage structure.
-   **Custom Class Lists:**
    -   Implement functionality to paste a list of students from the clipboard.
    -   Implement functionality to save the class list with a custom name.
    -   Implement functionality to load previously saved class lists.

**2. Randomization Engine Module (`randomizer.py`):**

-   **Random Name Generation:**
    -   Implement basic random name generation without filters.
    -   Implement gender-based filtering.
    -   Implement attribute-based filtering (if applicable).
-   **Group Generation:**
    -   Implement group generation based on the number of groups.
    -   Implement group generation based on group size.
    -   Implement gender distribution control within groups.
    -   Implement representative picking functionality.

**3. UI Development (`ui.py`):**

-   **UI Framework Selection:**
    -   Select a UI framework.
-   **UI Design and Implementation:**
    -   Design the UI layout and elements.
    -   Implement input fields and controls for name generation and group formation parameters.
    -   Implement input fields and controls for custom class list management.
    -   Implement output display for generated names and groups.
    -   Connect UI elements to core functionalities in `data_manager.py` and `randomizer.py`.

**4. Testing:**

-   **Unit Testing:**
    -   Write unit tests for functions in `data_manager.py` (name dataset and custom class list management).
    -   Write unit tests for functions in `randomizer.py` (name generation and group generation).
-   **Integration Testing:**
    -   Conduct integration testing between the UI and core functionalities.
-   **User Acceptance Testing:**
    -   Plan and execute user acceptance testing.

**5. Documentation and Deployment:**

-   **Documentation:**
    -   Write a user manual or help documentation.
    -   Add code comments and docstrings to all modules.
-   **Deployment:**
    -   Research and select a deployment method.
    -   Package and deploy the application.








