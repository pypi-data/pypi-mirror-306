import json
import os
import logging
from typing import Dict, Set, Optional

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set log level as needed

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Define directories
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
MAPPING_FILE = os.path.join(os.path.dirname(__file__), "mappings", "key_mapping.json")


def load_template(template_name: str) -> dict:
    """
    Load the JSON file for the specified template name.

    Args:
        template_name (str): Name of the template to load (without extension).

    Returns:
        dict: Contents of the template.

    Raises:
        FileNotFoundError: If the template file does not exist.
        json.JSONDecodeError: If the JSON parsing fails.
    """
    file_path = os.path.join(TEMPLATE_DIR, f"{template_name}.json")
    logger.debug(f"Attempting to load template '{template_name}' from '{file_path}'.")
    if not os.path.exists(file_path):
        logger.error(f"Template file '{template_name}.json' not found in '{TEMPLATE_DIR}'.")
        raise FileNotFoundError(f"{template_name}.json not found.")
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            template = json.load(f)
            logger.debug(f"Template '{template_name}' loaded successfully.")
            return template
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed for template '{template_name}': {str(e)}")
            raise


def load_key_mapping() -> Dict[str, str]:
    """
    Load the key mapping from the key_mapping.json file.

    Returns:
        Dict[str, str]: Mapping from internal keys to labels.

    Raises:
        FileNotFoundError: If the mapping file does not exist.
        json.JSONDecodeError: If the JSON parsing fails.
    """
    if not os.path.exists(MAPPING_FILE):
        logger.error(f"Key mapping file '{MAPPING_FILE}' not found.")
        raise FileNotFoundError(f"Key mapping file '{MAPPING_FILE}' not found.")
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        try:
            key_mapping = json.load(f)
            logger.debug(f"Key mapping loaded successfully from '{MAPPING_FILE}'.")
            return key_mapping
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed for key mapping file '{MAPPING_FILE}': {str(e)}")
            raise


def calculate_match_score(data_keys: Set[str], template_fields: Dict) -> int:
    """
    Calculate the number of matching keys between data and template fields based on labels.

    Args:
        data_keys (Set[str]): Set of data keys (labels).
        template_fields (Dict): Template field information.

    Returns:
        int: Number of matches.
    """
    template_labels = set(field_info["label"] for field_info in template_fields.values())
    score = len(data_keys & template_labels)
    logger.debug(f"Matching data keys {data_keys} with template labels {template_labels}: Score {score}")
    return score


def auto_detect_template(data: Dict, reverse_key_mapping: Dict[str, str], required_score: int = 3) -> str:
    """
    Automatically select the best template based on the data keys.

    Args:
        data (Dict): Data to be mapped.
        reverse_key_mapping (Dict[str, str]): Mapping from labels to internal keys.
        required_score (int): Minimum number of matches required to select a template.

    Returns:
        str: Name of the selected template.

    Raises:
        ValueError: If no suitable template is found.
    """
    if not data:
        logger.error("Input data is empty.")
        raise ValueError("Input data is empty. Please provide at least one field.")

    best_match = None
    highest_score = 0
    required_score = 3  # Example threshold; adjust as needed

    logger.debug(f"Starting template detection with data keys: {set(data.keys())}")

    for template_file in os.listdir(TEMPLATE_DIR):
        if template_file.endswith(".json"):
            template_name = template_file.replace(".json", "")
            try:
                template = load_template(template_name)
                # Get template labels
                template_labels = set(field_info["label"] for field_info in template.get("fields", {}).values())
                # Calculate score
                score = len(set(data.keys()) & template_labels)
                logger.debug(f"Template '{template_name}' has a match score of {score}.")
                if score > highest_score and score >= required_score:
                    highest_score = score
                    best_match = template_name
                    logger.debug(f"Template '{template_name}' is now the best match with score {score}.")
            except Exception as e:
                logger.error(f"Error loading template '{template_name}': {str(e)}")

    if not best_match:
        # Identify missing required fields
        required_fields = set()
        for template_file in os.listdir(TEMPLATE_DIR):
            if template_file.endswith(".json"):
                try:
                    template = load_template(template_file.replace(".json", ""))
                    required = {field_info["label"] for field_info in template.get("fields", {}).values() if field_info.get("required", False)}
                    required_fields.update(required)
                except Exception as e:
                    logger.error(f"Error loading template '{template_file}': {str(e)}")

        missing = required_fields - set(data.keys())
        if missing:
            missing_str = ", ".join(missing)
            logger.warning(f"No suitable template found. Missing fields: {missing_str}")
            raise ValueError(f"No suitable template found. Missing fields: {missing_str}")
        else:
            logger.warning("No suitable template found.")
            raise ValueError("No suitable template found.")

    logger.info(f"Best match selected: '{best_match}' with a score of {highest_score}.")
    return best_match


class TemplateManager:
    def __init__(self, data_path='lingustruct/data/data.json'):
        self.data_path = data_path
        self.key_mapping = load_key_mapping()
        self.reverse_key_mapping = {v: k for k, v in self.key_mapping.items()}
        self.templates = self.load_templates()
        # Load templates for automatic mapping
        self.auto_mapping_templates = self.load_auto_mapping_templates()
        logger.debug("TemplateManager initialized successfully.")

    def load_templates(self) -> list:
        """
        Load the base templates data from the specified data path.

        Returns:
            list: List of template fields.

        Raises:
            FileNotFoundError: If the data file does not exist.
            json.JSONDecodeError: If the JSON parsing fails.
        """
        if not os.path.exists(self.data_path):
            logger.error(f"Data file '{self.data_path}' not found.")
            raise FileNotFoundError(f"{self.data_path} not found.")
        with open(self.data_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                logger.debug(f"Data file '{self.data_path}' loaded successfully.")
                return data.get('fields', [])
            except json.JSONDecodeError as e:
                logger.error(f"JSON decoding failed for data file '{self.data_path}': {str(e)}")
                raise

    def load_auto_mapping_templates(self) -> Dict[str, dict]:
        """
        Load all templates from the template directory for automatic mapping.

        Returns:
            Dict[str, dict]: Dictionary with template names as keys and their contents.

        Raises:
            Exception: If loading any template fails.
        """
        templates = {}
        logger.debug(f"Loading templates from '{TEMPLATE_DIR}' for automatic mapping.")
        for template_file in os.listdir(TEMPLATE_DIR):
            if template_file.endswith(".json"):
                template_name = template_file.replace(".json", "")
                try:
                    templates[template_name] = load_template(template_name)
                    logger.debug(f"Loaded template for auto mapping: '{template_name}'.")
                except Exception as e:
                    logger.error(f"Failed to load template '{template_name}': {str(e)}")
        logger.info(f"Total templates loaded for auto mapping: {len(templates)}.")
        return templates

    def get_field(self, field_name: str) -> Optional[dict]:
        """
        Retrieve a field by its name from the loaded templates.

        Args:
            field_name (str): The name of the field to retrieve.

        Returns:
            Optional[dict]: The field dictionary if found, else None.
        """
        for field in self.templates:
            if field['name'] == field_name:
                logger.debug(f"Field '{field_name}' found.")
                return field
        logger.debug(f"Field '{field_name}' not found.")
        return None

    def add_field(self, field: dict):
        """
        Add a new field to the templates and save the updated templates.

        Args:
            field (dict): The field to add.
        """
        self.templates.append(field)
        logger.debug(f"Adding new field: {field}")
        self.save_templates()

    def save_templates(self):
        """
        Save the current templates to the data path.
        """
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump({"fields": self.templates}, f, ensure_ascii=False, indent=4)
        logger.debug(f"Templates saved successfully to '{self.data_path}'.")

    def auto_map_data(self, data: dict) -> dict:
        """
        Automatically map the data to the most suitable template.

        Args:
            data (dict): Data to be mapped.

        Returns:
            dict: Selected template name and mapped data.

        Raises:
            ValueError: If no suitable template is found or template is not loaded.
        """
        logger.debug(f"Starting auto_map_data with input data: {data}")
        template_name = auto_detect_template(data, self.reverse_key_mapping)
        template = self.auto_mapping_templates.get(template_name)

        if not template:
            logger.error(f"Template '{template_name}' is not loaded.")
            raise ValueError(f"Template '{template_name}' is not loaded.")

        logger.debug(f"Mapping data using template '{template_name}'.")

        # Create a mapping of labels to keys from the template fields
        mapping = {field_info["label"]: key for key, field_info in template.get("fields", {}).items()}
        logger.debug(f"Field label to key mapping: {mapping}")

        # Map the data keys (labels) to template keys
        mapped_data = {}
        for k, v in data.items():
            if k in mapping:
                mapped_key = mapping[k]
                mapped_data[mapped_key] = v
                logger.debug(f"Mapping '{k}' to '{mapped_key}' with value '{v}'.")
            else:
                # If the key is not in the mapping, keep it as is
                mapped_data[k] = v
                logger.debug(f"No mapping found for '{k}'. Keeping as is.")

        logger.info(f"Data mapped using template '{template_name}': {mapped_data}")

        return {"template": template_name, "mapped_data": mapped_data}
