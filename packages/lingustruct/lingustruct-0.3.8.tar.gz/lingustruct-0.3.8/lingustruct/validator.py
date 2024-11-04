import os
import json
from jsonschema import validate, ValidationError

class Validator:
    def __init__(self):
        """全てのスキーマファイルをロード"""
        self.schemas = self.load_all_schemas()

    def load_all_schemas(self):
        """テンプレートディレクトリ内の全てのスキーマをロード"""
        schemas = {}
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")

        # ディレクトリ内のすべてのスキーマファイルを読み込む
        for filename in os.listdir(templates_dir):
            if filename.endswith("_s.json"):
                template_id = filename.split("_")[0].replace("m", "")
                with open(os.path.join(templates_dir, filename), "r", encoding="utf-8") as f:
                    schemas[template_id] = json.load(f)

        return schemas

    def validate(self, data, template_id):
        """指定されたテンプレートIDのスキーマでデータを検証"""
        if template_id not in self.schemas:
            raise ValueError(f"Template ID {template_id} not found.")

        schema = self.schemas[template_id]

        try:
            validate(instance=data, schema=schema)
            return True, "Validation successful"
        except ValidationError as e:
            return False, f"Validation failed: {e.message}"
