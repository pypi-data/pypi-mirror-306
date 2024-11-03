from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.builders.phases import Phase


class Plan(Base):

    def __init__(
        self,
        name: str,
        product: Product,
        initial_phases: List[Phase],
        final_phase: Phase,
        pretty_name: str = None,
    ) -> None:
        """Create the XML representation of the plan"""

        self.name = name
        self.product = product
        self.initial_phases = initial_phases
        self.final_phase = final_phase
        self.pretty_name = pretty_name
        self.to_xml()

    def to_xml(self):

        root = ET.Element("plan")
        root.set("name", self.name)

        if self.pretty_name:
            root.set("prettyName", self.pretty_name)

        product_element = ET.SubElement(root, "product")
        product_element.text = self.product.name

        initial_phases_element = ET.SubElement(root, "initialPhases")
        for phase in self.initial_phases:
            initial_phases_element.append(phase.element)

        final_phases_element = ET.SubElement(root, "finalPhase")
        final_phases_element.set("type", str(self.final_phase.type))

        final_phases_element.append(self.final_phase.duration.element)

        if self.final_phase.fixed_price:
            final_phases_element.append(self.final_phase.fixed_price.element)

        if self.final_phase.recurring_price:
            final_phases_element.append(self.final_phase.recurring_price.element)

        self.element = root
