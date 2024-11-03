from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import TimeUnit, BillingPeriod, PhaseType
from killbill_xml_builder.builders.prices import Price


class Duration(Base):

    def __init__(self, length: int = 0, time_unit: TimeUnit = TimeUnit.DAYS) -> None:
        """Create the XML representation of the duration"""
        self.length = str(length)
        self.time_unit = time_unit
        self.to_xml()

    def to_xml(self):

        root = ET.Element("duration")

        unit_element = ET.SubElement(root, "unit")
        unit_element.text = str(self.time_unit)

        if self.time_unit != TimeUnit.UNLIMITED:

            number_element = ET.SubElement(root, "number")
            number_element.text = self.length

        self.element = root


class RecurringPrice(Base):
    def __init__(self, prices: List[Price], billing_period: BillingPeriod) -> None:
        """Create the XML representation of the recurring price"""
        self.prices = prices
        self.billing_period = billing_period
        self.to_xml()

    def to_xml(self):

        root = ET.Element("recurring")

        billing_period_element = ET.SubElement(root, "billingPeriod")
        billing_period_element.text = str(self.billing_period)

        recurring_price_element = ET.SubElement(root, "recurringPrice")
        for price in self.prices:
            recurring_price_element.append(price.element)

        self.element = root


class FixedPrice(Base):
    def __init__(self, prices: List[Price] = []) -> None:
        """Create the XML representation of the fixed price"""
        self.prices = prices
        self.to_xml()

    def to_xml(self):

        root = ET.Element("fixed")

        fixed_price_element = ET.SubElement(root, "fixedPrice")
        for price in self.prices:
            fixed_price_element.append(price.element)

        self.element = root


class Phase(Base):
    def __init__(
        self,
        type: PhaseType,
        duration: Duration,
        recurring_price: RecurringPrice = None,
        fixed_price: FixedPrice = None,
    ) -> None:
        """Create the XML representation of the phase"""

        self.type = type
        self.duration = duration
        self.recurring_price = recurring_price
        self.fixed_price = fixed_price
        self.to_xml()

    def to_xml(self):

        root = ET.Element("phase")
        root.set("type", str(self.type))

        root.append(self.duration.element)

        if self.fixed_price:
            root.append(self.fixed_price.element)

        if self.recurring_price:
            root.append(self.recurring_price.element)

        self.element = root
