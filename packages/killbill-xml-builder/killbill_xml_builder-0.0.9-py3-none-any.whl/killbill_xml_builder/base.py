import abc
from xml.etree import ElementTree as ET


class Base:
    def __init__(self):
        self.element = None
        self.to_xml()

    @abc.abstractmethod
    def to_xml(self):
        """Create the XML representation of the object"""

    def __str__(self):
        return ET.tostring(self.element, encoding="unicode")

    def write(self, filename: str = "element.xml"):
        """Save as file"""
        tree = ET.ElementTree(self.element)
        tree.write(filename)
