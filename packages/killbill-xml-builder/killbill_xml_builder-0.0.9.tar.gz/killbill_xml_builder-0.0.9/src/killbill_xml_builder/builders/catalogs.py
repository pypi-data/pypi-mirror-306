from typing import List
import datetime
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import BillingMode
from killbill_xml_builder.builders.currencies import Currencies
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.builders.plans import Plan
from killbill_xml_builder.builders.rules import Rules
from killbill_xml_builder.utils import get_effective_date


class Catalog(Base):

    def __init__(
        self,
        name: str,
        billing_mode: BillingMode,
        currencies: Currencies,
        products: List[Product],
        rules: Rules,
        plans: List[Plan],
        effective_date: str = None,
    ) -> None:
        """Create the XML representation of the catalog"""

        if effective_date is None:
            self.effective_date = get_effective_date()
        else:
            self.effective_date = effective_date

        self.name = name
        self.billing_mode = billing_mode
        self.currencies = currencies
        self.products = products
        self.plans = plans
        self.rules = rules
        self.to_xml()

    def to_xml(self):

        root = ET.Element("catalog")

        effective_date_element = ET.SubElement(root, "effectiveDate")
        effective_date_element.text = self.effective_date

        catalog_name_element = ET.SubElement(root, "catalogName")
        catalog_name_element.text = self.name

        recurring_billing_mode = ET.SubElement(root, "recurringBillingMode")
        recurring_billing_mode.text = str(self.billing_mode)

        root.append(self.currencies.element)

        products_element = ET.SubElement(root, "products")
        for product in self.products:
            products_element.append(product.element)

        root.append(self.rules.element)

        plans_element = ET.SubElement(root, "plans")
        for plan in self.plans:
            plans_element.append(plan.element)

        price_lists_element = ET.SubElement(root, "priceLists")

        def_price_list_element = ET.SubElement(price_lists_element, "defaultPriceList")
        def_price_list_element.set("name", "DEFAULT")

        plans_list_element = ET.SubElement(def_price_list_element, "plans")
        for plan in self.plans:
            plan_element = ET.SubElement(plans_list_element, "plan")
            plan_element.text = plan.name

        self.element = root

    def write(self, filename: str = "catalog.xml"):
        return super().write(filename)
