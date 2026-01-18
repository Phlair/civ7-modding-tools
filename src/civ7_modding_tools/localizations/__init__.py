"""Localization classes for mod entities."""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class BaseLocalization(BaseModel):
    """Base class for all localizations."""

    model_config = ConfigDict(extra="allow")

    def __repr__(self) -> str:
        """String representation."""
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.model_dump().items()
        )
        return f"{self.__class__.__name__}({attrs})"
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Convert localization to node data."""
        return []


class CivilizationLocalization(BaseLocalization):
    """Localization for civilizations."""
    name: Optional[str] = None
    description: Optional[str] = None
    full_name: Optional[str] = None
    adjective: Optional[str] = None
    city_names: Optional[List[str]] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for civilization localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({
                "tag": locale(prefix, "description"),
                "text": self.description,
            })
        if self.full_name:
            nodes.append({"tag": locale(prefix, "fullName"), "text": self.full_name})
        if self.adjective:
            nodes.append({"tag": locale(prefix, "adjective"), "text": self.adjective})
        if self.city_names:
            for i, city_name in enumerate(self.city_names, 1):
                nodes.append({
                    "tag": locale(prefix, f"cityNames_{i}"),
                    "text": city_name,
                })
        return nodes


class UnitLocalization(BaseLocalization):
    """Localization for units."""
    name: Optional[str] = None
    description: Optional[str] = None
    unique_name: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for unit localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        if self.unique_name:
            nodes.append({"tag": locale(prefix, "uniqueName"), "text": self.unique_name})
        return nodes


class ConstructibleLocalization(BaseLocalization):
    """Localization for buildings and improvements."""
    name: Optional[str] = None
    description: Optional[str] = None
    unique_name: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for constructible localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        if self.unique_name:
            nodes.append({"tag": locale(prefix, "uniqueName"), "text": self.unique_name})
        return nodes


class ProgressionTreeLocalization(BaseLocalization):
    """Localization for progression trees."""
    name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for progression tree localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


class ProgressionTreeNodeLocalization(BaseLocalization):
    """Localization for progression tree nodes."""
    name: Optional[str] = None
    description: Optional[str] = None
    quote: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for progression tree node localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        if self.quote:
            nodes.append({"tag": locale(prefix, "quote"), "text": self.quote})
        return nodes


class ModifierLocalization(BaseLocalization):
    """Localization for modifiers."""
    name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for modifier localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


class TraditionLocalization(BaseLocalization):
    """Localization for traditions."""
    name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for tradition localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


class LeaderUnlockLocalization(BaseLocalization):
    """Localization for leader unlocks."""
    leader_name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for leader unlock localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.leader_name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.leader_name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


class CivilizationUnlockLocalization(BaseLocalization):
    """Localization for civilization unlocks."""
    name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for civilization unlock localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


class UniqueQuarterLocalization(BaseLocalization):
    """Localization for unique quarters."""
    name: Optional[str] = None
    description: Optional[str] = None
    
    def get_nodes(self, entity_id: str) -> list[dict]:
        """Generate nodes for unique quarter localization."""
        from utils import locale
        nodes = []
        prefix = entity_id.upper()
        
        if self.name:
            nodes.append({"tag": locale(prefix, "name"), "text": self.name})
        if self.description:
            nodes.append({"tag": locale(prefix, "description"), "text": self.description})
        return nodes


__all__ = [
    "BaseLocalization",
    "CivilizationLocalization",
    "UnitLocalization",
    "ConstructibleLocalization",
    "ProgressionTreeLocalization",
    "ProgressionTreeNodeLocalization",
    "ModifierLocalization",
    "TraditionLocalization",
    "LeaderUnlockLocalization",
    "CivilizationUnlockLocalization",
    "UniqueQuarterLocalization",
]
