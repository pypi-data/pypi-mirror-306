from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import ProductCategory


class Product(Base):

    def __init__(
        self,
        name: str,
        category: ProductCategory = ProductCategory.BASE,
        available: list = None,
        included: List = None,
        pretty_name: str = None,
    ) -> None:
        """Create the XML representation of the product"""

        self.name = name
        self.pretty_name = pretty_name
        self.category = category
        self.available = available
        self.included = included
        self.to_xml()

    def to_xml(self):

        root = ET.Element("product")
        root.set("name", self.name)

        if self.pretty_name:
            root.set("prettyName", self.pretty_name)

        category_element = ET.SubElement(root, "category")
        category_element.text = str(self.category)

        if self.included:
            included_element = ET.SubElement(root, "included")
            for ie in self.included:
                addon_product = ET.SubElement(included_element, "addonProduct")
                addon_product.text = ie if isinstance(ie, str) else ie.name

        if self.available:
            available_element = ET.SubElement(root, "available")
            for ae in self.available:
                addon_product = ET.SubElement(available_element, "addonProduct")
                addon_product.text = ae if isinstance(ae, str) else ae.name

        self.element = root
