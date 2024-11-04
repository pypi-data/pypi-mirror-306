import json
import os
from jsonschema import validate, ValidationError, SchemaError
from jinja2 import Environment, FileSystemLoader
from typing import Any, Dict, List, Optional
from .converters import (
    lingu_struct_to_human_readable,
    human_readable_to_lingu_struct,
    lingu_struct_to_markdown,
    markdown_to_human_readable
)

class LinguStruct:
    def __init__(self, template_dir: Optional[str] = None):
        """
        LinguStruct の初期化。

        Args:
            template_dir (Optional[str]): テンプレートディレクトリのパス。指定されない場合はデフォルトのパスを使用。
        """
        if template_dir is None:
            # テンプレートディレクトリのパスを初期化
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template_dir = template_dir

    def generate_master_json(self, replacements: Dict[str, Any], output_path: str = 'master.json') -> None:
        """
        master_template.json を使って master.json を生成する。

        Args:
            replacements (Dict[str, Any]): テンプレートに埋め込むデータ。
            output_path (str): 生成する master.json の出力パス。
        """
        template = self.env.get_template('master_template.json')
        rendered = template.render(replacements)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)

    def generate_overview_json(self, replacements: Dict[str, Any], output_path: str = 'overview.json') -> None:
        """
        overview_template.json を使って overview.json を生成する。

        Args:
            replacements (Dict[str, Any]): テンプレートに埋め込むデータ。
            output_path (str): 生成する overview.json の出力パス。
        """
        template = self.env.get_template('overview_template.json')
        rendered = template.render(replacements)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)

    def load_module(self, module_id: int, project_dir: str = 'src') -> Dict[str, Any]:
        """
        指定した ID のモジュールをロードする。

        Args:
            module_id (int): ロードするモジュールの ID。
            project_dir (str): プロジェクトディレクトリのパス。

        Returns:
            Dict[str, Any]: ロードしたモジュールのデータ。

        Raises:
            FileNotFoundError: モジュールファイルが見つからない場合。
            ValueError: モジュールファイルが無効な JSON 形式の場合。
            Exception: その他の予期せぬエラーが発生した場合。
        """
        module_path = os.path.join(project_dir, 'lingustruct', 'templates', f'm{module_id}.json')
        print(f"Loading module from: {module_path}")  # デバッグ用

        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Module {module_id} not found at {module_path}.")

        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Successfully loaded module {module_id}")  # デバッグ用
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in module {module_id}: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while loading module {module_id}: {str(e)}")

    def validate_module(self, module_id: int, schema_path: str) -> bool:
        """
        モジュールの JSON をスキーマで検証する。

        Args:
            module_id (int): 検証するモジュールの ID。
            schema_path (str): スキーマファイルのパス。

        Returns:
            bool: 検証が成功した場合は True。

        Raises:
            ValueError: スキーマに基づく検証エラーが発生した場合。
            FileNotFoundError: スキーマファイルが見つからない場合。
            Exception: その他の予期せぬエラーが発生した場合。
        """
        try:
            module_data = self.load_module(module_id)
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            validate(instance=module_data, schema=schema)
            print(f"Module {module_id} is valid according to the schema.")
            return True
        except ValidationError as e:
            raise ValueError(f"Validation error in module {module_id}: {e.message}")
        except SchemaError as e:
            raise ValueError(f"Invalid schema: {e.message}")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e.filename}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def convert_to_human_readable(self, lingu_struct_data: Dict[str, Any], key_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        LinguStruct データを人間が読める形式に変換する。

        Args:
            lingu_struct_data (Dict[str, Any]): LinguStruct の JSON データ。
            key_mapping (Dict[str, str]): キーマッピング。

        Returns:
            Dict[str, Any]: 人間が読める形式のデータ。
        """
        return lingu_struct_to_human_readable(lingu_struct_data, key_mapping)

    def convert_from_human_readable(self, human_readable_data: Dict[str, Any], key_mapping_reverse: Dict[str, str]) -> Dict[str, Any]:
        """
        人間が読める形式のデータを LinguStruct 形式に変換する。

        Args:
            human_readable_data (Dict[str, Any]): 人間が読める形式のデータ。
            key_mapping_reverse (Dict[str, str]): 逆キーマッピング。

        Returns:
            Dict[str, Any]: LinguStruct 形式のデータ。
        """
        return human_readable_to_lingu_struct(human_readable_data, key_mapping_reverse)

    def convert_to_markdown(self, lingu_struct_data: Dict[str, Any], key_mapping: Dict[str, str]) -> str:
        """
        LinguStruct データを Markdown 形式に変換する。

        Args:
            lingu_struct_data (Dict[str, Any]): LinguStruct の JSON データ。
            key_mapping (Dict[str, str]): キーマッピング。

        Returns:
            str: Markdown 形式のテキスト。
        """
        return lingu_struct_to_markdown(lingu_struct_data, key_mapping)

    def convert_from_markdown(self, markdown_text: str, key_mapping_reverse: Dict[str, str]) -> Dict[str, Any]:
        """
        Markdown 形式のデータを人間が読める形式に変換する。

        Args:
            markdown_text (str): Markdown 形式のテキスト。
            key_mapping_reverse (Dict[str, str]): 逆キーマッピング。

        Returns:
            Dict[str, Any]: 人間が読める形式のデータ。
        """
        return markdown_to_human_readable(markdown_text, key_mapping_reverse)
