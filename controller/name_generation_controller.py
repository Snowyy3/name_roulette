from model.name_generator import NameGenerator
import logging

logger = logging.getLogger(__name__)


class NameGenerationController:
    def __init__(self, list_controller=None):
        self.name_generator = NameGenerator()
        self.list_controller = list_controller

    def validate_input(
        self,
        names_text: str,
        selected_num: str,
        custom_value: str,
        selected_gender_filter: str = "none",
        male_count: str = "0",
        female_count: str = "0",
    ) -> bool:
        """Validate user input for name generation."""
        try:
            # Get names without gender info for basic validation
            names = [name.strip() for name in names_text.strip().splitlines() if name.strip()]
            if not names:
                return False

            # Validate basic requirements
            total_count = self.name_generator.get_num_names(selected_num, custom_value)
            if total_count <= 0 or total_count > len(names):
                return False

            # For gender-specific validation
            if selected_gender_filter != "none":
                try:
                    male_count = int(male_count) if selected_gender_filter == "male" else 0
                    female_count = int(female_count) if selected_gender_filter == "female" else 0
                    total_requested = male_count + female_count
                    
                    # Check if total gender counts exceed total requested
                    if total_requested > total_count:
                        return False
                        
                except ValueError:
                    return False

            return True
            
        except Exception as e:
            logger.error(f"Error in validate_input: {e}")
            return False

    def generate_names(
        self,
        names_text: str,
        genders_text: str,
        selected_num: str,
        custom_value: str,
        selected_gender_filter: str,
        male_count: str = "0",
        female_count: str = "0",
    ) -> list[str]:
        """Handle name generation logic."""
        total_count = self.name_generator.get_num_names(selected_num, custom_value)

        if selected_gender_filter == "none":
            return self.name_generator.generate_random_names_without_gender(
                names_text=names_text, total_count=total_count
            )

        try:
            male_count = int(male_count) if selected_gender_filter == "male" else 0
            female_count = int(female_count) if selected_gender_filter == "female" else 0
        except ValueError:
            male_count = female_count = 0

        return self.name_generator.process_name_generation(
            names_text=names_text,
            genders_text=genders_text,
            selected_num=selected_num,
            custom_value=custom_value,
            male_count=male_count,
            female_count=female_count,
        )

    def get_active_list(self):
        """Get the currently selected list from the list controller."""
        if self.list_controller:
            return self.list_controller.get_selected_list()
        return None

    def format_list_data(self, list_data):
        """Format list data for display."""
        if not list_data:
            return [], []

        items = list_data.items
        names = [item.get("name", "") for item in items]
        genders = [item.get("gender", "") for item in items]
        return names, genders

    def update_selected_num(self, selected_num: str, custom_value: str) -> tuple[bool, str]:
        """Handle number selection logic."""
        if selected_num == "custom":
            return True, custom_value
        return False, ""

    def update_gender_filter(self, filter_type: str) -> dict[str, bool]:
        """Handle gender filter state updates."""
        states = {"male_input": False, "female_input": False, "gender_visible": False}

        if filter_type == "male":
            states["male_input"] = True
            states["gender_visible"] = True
        elif filter_type == "female":
            states["female_input"] = True
            states["gender_visible"] = True

        return states

    def should_play_sound(self, action: str) -> bool:
        """Determine if sound should be played."""
        return action in ["randomize", "clear"]

    def format_output_label(self, names: list[str]) -> str:
        """Format the output label based on number of names."""
        return "Generated names:" if len(names) > 1 else "Generated name:"

    def handle_clipboard_copy(self, text: str) -> bool:
        """Handle clipboard copy operation."""
        return bool(text)
