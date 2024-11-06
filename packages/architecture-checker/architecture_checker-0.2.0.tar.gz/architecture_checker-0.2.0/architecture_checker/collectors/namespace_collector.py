from pathlib import Path
from typing import Set
from .base_collector import BaseCollector
from ..utils.module_utils import get_modules_in_project


class NamespaceCollector(BaseCollector):
    def __init__(self, config: dict, project_root: Path):
        self.namespace = config.get("name", "")
        self.project_root = project_root

    def collect(self) -> Set[Path]:
        modules = get_modules_in_project(self.project_root)
        matched_files = {path for mod_name, path in modules.items() if mod_name.startswith(self.namespace)}
        return matched_files
