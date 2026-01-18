"""Criteria and ActionGroup nodes for mod loading control."""

from typing import Optional
from uuid import uuid4
from civ7_modding_tools.nodes.base import BaseNode


class CriteriaNode(BaseNode):
    """
    Represents criteria for when mod content should be loaded.
    
    Criteria determine the conditions under which action groups activate,
    typically based on game ages (Antiquity, Medieval, Modern, etc).
    """
    
    _name: str = "Criteria"
    
    id: Optional[str] = None
    any: Optional[bool] = None
    ages: list[str] = []
    
    def __init__(self, payload: dict | None = None) -> None:
        """Initialize CriteriaNode with optional payload."""
        super().__init__()
        if self.id is None:
            self.id = str(uuid4())
        if payload:
            self.fill(payload)
    
    def to_xml_element(self) -> dict:
        """
        Generate Criteria XML element.
        
        Returns XML with id, optional any attribute, and age/AlwaysMet content.
        """
        attrs = {"id": self.id}
        
        if self.any:
            attrs["any"] = "true"
        
        # Create content - ages if present, otherwise AlwaysMet
        content = {}
        if self.ages:
            content = {"AgeInUse": [{"_attrs": {"type": age}} for age in self.ages]}
        else:
            content = {"AlwaysMet": None}
        
        return {
            "_name": self._name,
            "_attrs": attrs,
            "_content": content,
        }


class ActionGroupNode(BaseNode):
    """
    Represents an ActionGroup that bundles mod content loading.
    
    Action groups specify when content is loaded (always, in specific ages,
    or under specific criteria). Each action group has an ID, scope (game/shell),
    and associated criteria.
    """
    
    _name: str = "ActionGroup"
    
    id: Optional[str] = None
    scope: Optional[str] = None  # "game" or "shell"
    criteria: Optional[CriteriaNode] = None
    
    def __init__(self, payload: dict | None = None) -> None:
        """Initialize ActionGroupNode with optional payload."""
        super().__init__()
        if self.id is None:
            self.id = str(uuid4())
        if self.scope is None:
            self.scope = "game"
        if self.criteria is None:
            self.criteria = CriteriaNode()
        if payload:
            self.fill(payload)
    
    def to_xml_element(self) -> dict:
        """
        Generate ActionGroup XML element.
        
        Returns XML with id, scope, and nested Criteria element.
        """
        attrs = {}
        if self.id:
            attrs["id"] = self.id
        if self.scope:
            attrs["scope"] = self.scope
        
        content = {}
        if self.criteria:
            criteria_xml = self.criteria.to_xml_element()
            if criteria_xml:
                content["Criteria"] = criteria_xml
        
        return {
            "_name": self._name,
            "_attrs": attrs,
            "_content": content,
        }
