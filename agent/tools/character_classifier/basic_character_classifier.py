from typing import Tuple, Optional, List, Dict
from agent.tools.character_classifier.character_loader import get_character_loader

class BasicCharacterClassifier:
    """
    basic character classifier that checks if a query involves characters from "凡人修仙传" and extracts relevant information. It uses a predefined character map with aliases to identify mentions in the query.
    """
    
    def __init__(self):
        self.loader = get_character_loader()
        self.all_aliases = self.loader.get_all_aliases()
        self.all_characters = self.loader.get_all_characters()
    
    def classify(self, query: str) -> Tuple[bool, Optional[Dict]]:
        """
        Classify if the query involves "凡人修仙传" characters and extract details.
        
        Args:
            query: 
            
        Returns:
            
        """
        mentioned = self.loader.find_all_characters(query)
        
        if mentioned:
            matched_details = []
            for char_name in mentioned:
                char_info = self.loader.get_character_info(char_name)
                matched_details.append({
                    "character": char_name,
                    "info": char_info
                })
            
            return True, {
                "type": "character",
                "matched": matched_details,
                "original_query": query
            }
        
        return False, None
    
    def get_character_from_query(self, query: str) -> List[str]:
        return self.loader.find_character_by_alias(query)

