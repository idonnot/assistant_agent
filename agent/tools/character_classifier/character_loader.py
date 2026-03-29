import json
import os
from typing import Dict, List, Optional
from config.settings import FANREN_CHARACTER_MAP_PATH

class CharacterLoader:
    def __init__(self, json_path: str = None):
        if json_path is None:
            json_path = FANREN_CHARACTER_MAP_PATH
        
        self.json_path = json_path
        self.characters = self._load_json()
        self.alias_to_name = self._build_alias_map()
    
    def _load_json(self) -> Dict:
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Charater map doesn't exist: {self.json_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Wrong Json format: {self.json_path}")
            return {}
    
    def _build_alias_map(self) -> Dict[str, str]:
        alias_map = {}
        for char_name, char_info in self.characters.items():
            for alias in char_info.get("aliases", []):
                alias_map[alias] = char_name
        return alias_map
    
    def get_all_characters(self) -> List[str]:
        return list(self.characters.keys())
    
    def get_all_aliases(self) -> List[str]:
        return list(self.alias_to_name.keys())
    
    def find_character_by_alias(self, text: str) -> List[str]:
        found = []
        for alias, char_name in self.alias_to_name.items():
            if alias in text and char_name not in found:
                found.append(char_name)
        return found
    
    def find_all_characters(self, text: str) -> List[str]:
        found = []
        for alias, char_name in self.alias_to_name.items():
            if alias in text and char_name not in found:
                found.append(char_name)
        return found
    
    def get_character_info(self, char_name: str) -> Dict:
        return self.characters.get(char_name, {})
    


_character_loader = None

def get_character_loader():
    global _character_loader
    if _character_loader is None:
        _character_loader = CharacterLoader()
    return _character_loader