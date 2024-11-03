from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.enums import (
    BillingPolicy,
    EntitlementPolicy,
    PhaseType,
    ProductCategory,
    BillingPeriod,
    BillingAlignmentPolicy,
    CreateAlignmentPolicy,
    ChangeAlignmentPolicy,
)


class CreationContext(Base):
    """Creation Context - provides the context for a new subscription"""

    def __init__(
        self,
        product: Product = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
    ) -> None:

        self.product = product
        self.product_category = product_category
        self.billing_period = billing_period
        self.price_list = price_list
        self.to_xml()

    def to_xml(self):

        elements = []

        if self.product:
            product_element = ET.Element("product")
            product_element.text = self.product.name
            elements.append(product_element)

        if self.product_category:
            product_category_element = ET.Element("productCategory")
            product_category_element.text = str(self.product_category)
            elements.append(product_category_element)

        if self.billing_period:
            billing_period_element = ET.Element("billingPeriod")
            billing_period_element.text = str(self.billing_period)
            elements.append(billing_period_element)

        if self.price_list:
            price_list_element = ET.Element("priceList")
            price_list_element.text = self.price_list
            elements.append(price_list_element)

        return elements


class SubscriptionContext(Base):
    """
    Subscription Context - provides the context of an existing subscription,
    including details of the plan, phase, pricelist, product etc.
    """

    def __init__(
        self,
        product: Product = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
        phase_type: PhaseType = None,
    ) -> None:

        self.product = product
        self.product_category = product_category
        self.billing_period = billing_period
        self.price_list = price_list
        self.phase_type = phase_type
        self.to_xml()

    def to_xml(self):

        elements = []

        if self.product:
            product_element = ET.Element("product")
            product_element.text = self.product.name
            elements.append(product_element)

        if self.product_category:
            product_category_element = ET.Element("productCategory")
            product_category_element.text = str(self.product_category)
            elements.append(product_category_element)

        if self.billing_period:
            billing_period_element = ET.Element("billingPeriod")
            billing_period_element.text = str(self.billing_period)
            elements.append(billing_period_element)

        if self.price_list:
            price_list_element = ET.Element("priceList")
            price_list_element.text = self.price_list
            elements.append(price_list_element)

        if self.phase_type:
            phase_type_element = ET.Element("phaseType")
            phase_type_element.text = str(self.phase_type)
            elements.append(phase_type_element)

        return elements


class ChangeContext(Base):
    """
    Change Context - provides the context not only about the phase
    of the current subscription but also details of the new target plan.
    This is used in the event of a plan change.
    """

    def __init__(
        self,
        phase_type: PhaseType = None,
        from_product: Product = None,
        from_product_category: ProductCategory = None,
        from_billing_period: BillingPeriod = None,
        from_price_list: str = None,
        to_product: Product = None,
        to_product_category: ProductCategory = None,
        to_billing_period: BillingPeriod = None,
        to_price_list: str = None,
    ):

        self.phase_type = phase_type
        self.from_product = from_product
        self.from_product_category = from_product_category
        self.from_billing_period = from_billing_period
        self.from_price_list = from_price_list
        self.to_product = to_product
        self.to_product_category = to_product_category
        self.to_billing_period = to_billing_period
        self.to_price_list = to_price_list
        self.to_xml()

    def to_xml(self):

        elements = []

        if self.phase_type:
            phase_type_element = ET.Element("phaseType")
            phase_type_element.text = str(self.phase_type)
            elements.append(phase_type_element)

        if self.from_product:
            from_product_element = ET.Element("fromProduct")
            from_product_element.text = self.from_product.name
            elements.append(from_product_element)

        if self.from_product_category:
            from_product_category_element = ET.Element("fromProductCategory")
            from_product_category_element.text = str(self.from_product_category)
            elements.append(from_product_category_element)

        if self.from_billing_period:
            from_billing_period_element = ET.Element("fromBillingPeriod")
            from_billing_period_element.text = str(self.from_billing_period)
            elements.append(from_billing_period_element)

        if self.from_price_list:
            from_price_list_element = ET.Element("fromPriceList")
            from_price_list_element.text = self.from_price_list
            elements.append(from_price_list_element)

        if self.to_product:
            to_product_element = ET.Element("toProduct")
            to_product_element.text = self.to_product.name
            elements.append(to_product_element)

        if self.to_product_category:
            to_product_category_element = ET.Element("toProductCategory")
            to_product_category_element.text = str(self.to_product_category)
            elements.append(to_product_category_element)

        if self.to_billing_period:
            to_billing_period_element = ET.Element("toBillingPeriod")
            to_billing_period_element.text = str(self.to_billing_period)
            elements.append(to_billing_period_element)

        if self.to_price_list:
            to_price_list_element = ET.Element("toPriceList")
            to_price_list_element.text = self.to_price_list
            elements.append(to_price_list_element)

        return elements


class ChangePolicyCase(ChangeContext):
    """Create the XML representation of the change policy case"""

    def __init__(
        self,
        policy: BillingPolicy,
        phase_type: PhaseType = None,
        from_product: Product = None,
        from_product_category: ProductCategory = None,
        from_billing_period: BillingPeriod = None,
        from_price_list: str = None,
        to_product: Product = None,
        to_product_category: ProductCategory = None,
        to_billing_period: BillingPeriod = None,
        to_price_list: str = None,
    ):
        self.policy = policy
        super().__init__(
            phase_type,
            from_product,
            from_product_category,
            from_billing_period,
            from_price_list,
            to_product,
            to_product_category,
            to_billing_period,
            to_price_list,
        )

    def to_xml(self):

        root = ET.Element("changePolicyCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        policy_element = ET.SubElement(root, "policy")
        policy_element.text = str(self.policy)

        self.element = root


class CancelPolicyCase(SubscriptionContext):
    """Create the XML representation of the cancel policy case"""

    def __init__(
        self,
        policy: EntitlementPolicy,
        product: Product = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
        phase_type: PhaseType = None,
    ) -> None:
        self.policy = policy
        super().__init__(
            product, product_category, billing_period, price_list, phase_type
        )

    def to_xml(self):

        root = ET.Element("cancelPolicyCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        policy_element = ET.SubElement(root, "policy")
        policy_element.text = str(self.policy)

        self.element = root


class BillingAlignmentCase(CreationContext):
    """Create the XML representation of the billing alignment case"""

    def __init__(
        self,
        alignment: BillingAlignmentPolicy,
        product: Product = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
    ) -> None:
        self.alignment = alignment
        super().__init__(product, product_category, billing_period, price_list)

    def to_xml(self):

        root = ET.Element("billingAlignmentCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        alignment_element = ET.SubElement(root, "alignment")
        alignment_element.text = str(self.alignment)

        self.element = root


class CreateAlignmentCase(CreationContext):
    """Create the XML representation of the billing alignment case"""

    def __init__(
        self,
        alignment: CreateAlignmentPolicy,
        product: Product = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
    ) -> None:
        self.alignment = alignment
        super().__init__(product, product_category, billing_period, price_list)

    def to_xml(self):

        root = ET.Element("createAlignmentCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        alignment_element = ET.SubElement(root, "alignment")
        alignment_element.text = str(self.alignment)

        self.element = root


class ChangeAlignmentCase(ChangeContext):
    """Create the XML representation of the change alignment case"""

    def __init__(
        self,
        alignment: ChangeAlignmentPolicy,
        phase_type: PhaseType = None,
        from_product: Product = None,
        from_product_category: ProductCategory = None,
        from_billing_period: BillingPeriod = None,
        from_price_list: str = None,
        to_product: Product = None,
        to_product_category: ProductCategory = None,
        to_billing_period: BillingPeriod = None,
        to_price_list: str = None,
    ):
        self.alignment = alignment
        super().__init__(
            phase_type,
            from_product,
            from_product_category,
            from_billing_period,
            from_price_list,
            to_product,
            to_product_category,
            to_billing_period,
            to_price_list,
        )

    def to_xml(self):

        root = ET.Element("changeAlignmentCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        alignment_element = ET.SubElement(root, "alignment")
        alignment_element.text = str(self.alignment)

        self.element = root


class PriceListCase(ChangeContext):
    """Create the XML representation of the price list case"""

    def __init__(
        self,
        phase_type: PhaseType = None,
        from_product: Product = None,
        from_product_category: ProductCategory = None,
        from_billing_period: BillingPeriod = None,
        from_price_list: str = None,
        to_product: Product = None,
        to_product_category: ProductCategory = None,
        to_billing_period: BillingPeriod = None,
        to_price_list: str = None,
    ):
        super().__init__(
            phase_type,
            from_product,
            from_product_category,
            from_billing_period,
            from_price_list,
            to_product,
            to_product_category,
            to_billing_period,
            to_price_list,
        )

    def to_xml(self):

        root = ET.Element("priceListCase")

        elements = super().to_xml()
        for element in elements:
            root.append(element)

        self.element = root


class Rules(Base):
    """Create the XML representation of the rule"""

    def __init__(
        self,
        change_policy_cases: List[ChangePolicyCase],
        cancel_policy_cases: List[CancelPolicyCase],
        billing_alignment_cases: List[BillingAlignmentCase] = None,
        create_alignment_cases: List[CreateAlignmentCase] = None,
        change_alignment_cases: List[ChangeAlignmentCase] = None,
        price_list_cases: List[PriceListCase] = None,
    ) -> None:

        self.change_policy_cases = change_policy_cases
        self.cancel_policy_cases = cancel_policy_cases
        self.billing_alignment_cases = billing_alignment_cases
        self.create_alignment_cases = create_alignment_cases
        self.change_alignment_cases = change_alignment_cases
        self.price_list_cases = price_list_cases
        self.to_xml()

    def to_xml(self):

        root = ET.Element("rules")

        change_policy_element = ET.SubElement(root, "changePolicy")
        for cpc in self.change_policy_cases:
            change_policy_element.append(cpc.element)

        cancel_policy_element = ET.SubElement(root, "cancelPolicy")
        for cpc in self.cancel_policy_cases:
            cancel_policy_element.append(cpc.element)

        if self.billing_alignment_cases:
            billing_alignment_element = ET.SubElement(root, "billingAlignment")
            for bac in self.billing_alignment_cases:
                billing_alignment_element.append(bac.element)

        if self.create_alignment_cases:
            create_alignment_element = ET.SubElement(root, "createAlignment")
            for cac in self.create_alignment_cases:
                create_alignment_element.append(cac.element)

        if self.change_alignment_cases:
            change_alignment_element = ET.SubElement(root, "changeAlignment")
            for cac in self.change_alignment_cases:
                change_alignment_element.append(cac.element)

        if self.price_list_cases :
            price_list_element = ET.SubElement(root, "priceList")
            for pl in self.price_list_cases:
                price_list_element.append(pl.element)
                
        self.element = root
