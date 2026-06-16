from __future__ import annotations

from dataclasses import dataclass, field
import xml.etree.ElementTree as ET
from typing import Self

@dataclass
class XMLHandler:
    """
    A class for handling XML files and elements.

    Attributes
    ----------
    xml : ET.ElementTree[ET.Element[str]]
        The parsed XML element tree.
    source : str, optional
        The source description of the XML (e.g., file path or identifier).
    xml_root : ET.Element
        The root element of the XML tree (initialized automatically).
    """
    xml: ET.ElementTree[ET.Element[str]]
    source: str = "<unknown>"
    xml_root: ET.Element = field(init=False)

    def __post_init__(self) -> None:
        """
        Initialize fields after the object is constructed.
        """
        self.xml_root = self.xml.getroot()

    def find(self, tag: str) -> str:
        """
        Find a tag under the root element.

        Parameters
        ----------
        tag : str
            The tag to find.

        Returns
        -------
        str
            The text content of the tag.

        Raises
        ------
        ValueError
            If the tag is not found.
        """
        find_result = self.xml_root.find(tag)
        if find_result is None:
            raise ValueError(f"Tag '{tag}' not found in {self.source}")
        return str(find_result.text) if find_result.text is not None else ""

    def find_nested_tags(
        self, 
        tags: list[str], 
        xml_element: ET.Element | None = None
    ) -> str:
        """
        Find nested tags starting from the root or a specified element.

        Parameters
        ----------
        tags : list[str]
            The sequence of tags to traverse.
        xml_element : ET.Element | None, optional
            The XML element to start from. If None, the root element is used.

        Returns
        -------
        str
            The text content of the deepest nested tag.

        Raises
        ------
        ValueError
            If the tags list is empty or any tag in the sequence is not found.
        """
        if xml_element is None:
            tags = tags.copy()
            xml_element = self.xml_root

        if not tags:
            raise ValueError("The tags list is empty.")

        tag = tags.pop(0)
        find_result = xml_element.find(tag)
        if find_result is None:
            raise ValueError(f"Tag '{tag}' not found in {self.source}")
        
        if len(tags) == 0:
            return str(find_result.text) if find_result.text is not None else ""
            
        return self.find_nested_tags(
            tags=tags, 
            xml_element=find_result
        )

    @classmethod
    def from_path(cls, xml_path: str) -> Self:
        """
        Create an XMLHandler instance from a file path.

        Parameters
        ----------
        xml_path : str
            The path to the XML file.

        Returns
        -------
        XMLHandler
            An instance of XMLHandler.
        """
        xml_tree = ET.parse(xml_path)
        return cls(xml=xml_tree, source=xml_path)