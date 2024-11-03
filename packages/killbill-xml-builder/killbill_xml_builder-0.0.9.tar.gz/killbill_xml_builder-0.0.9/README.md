# killbill-xml-builder

- [Installation](#installation)
- [Usage](#usage)
- [TODO](#todo)

### Installation

```bash
pip install killbill-xml-builder
```

### Usage

Import the required classes and create the catalog

```python
from killbill_xml_builder.enums import (
    PhaseType,
    TimeUnit,
    BillingPeriod,
    BillingMode,
    ProductCategory,
    BillingPolicy,
    EntitlementPolicy,
)

from killbill_xml_builder import (
    Currencies,
    Product,
    Phase,
    Price,
    Duration,
    FixedPrice,
    RecurringPrice,
    Plan,
    Catalog,
    Rules,
    ChangePolicyCase,
    CancelPolicyCase,
)
```

Create currencies

```python
currencies = Currencies(["USD", "GBP"])
```

Create add-on

```python
oil_slick = Product("OilSlick", ProductCategory.ADD_ON)

remote_control = Product("RemoteControl", ProductCategory.ADD_ON)
```

Create products

```python
standard = Product("Standard")

sports = Product("Sports", available=[oil_slick, remote_control])

super = Product("Super", included=[oil_slick], available=[remote_control])
```

Create products phases

Phase trial

```python
phase_trial = Phase(
    type=PhaseType.TRIAL,
    duration=Duration(length=30, time_unit=TimeUnit.DAYS),
    fixed_price=FixedPrice(),
)
```

Phase standard evergreen

```python
standard_evergreen = Phase(
    type=PhaseType.EVERGREEN,
    duration=Duration(time_unit=TimeUnit.UNLIMITED),
    recurring_price=RecurringPrice(
        prices=[Price("GBP", 75.00), Price("USD", 100.00)],
        billing_period=BillingPeriod.MONTHLY,
    ),
)
```

Phase sports evergreen

```python
sports_evergreen = Phase(
    type=PhaseType.EVERGREEN,
    duration=Duration(time_unit=TimeUnit.UNLIMITED),
    recurring_price=RecurringPrice(
        prices=[Price("GBP", 375.00), Price("USD", 500.00)],
        billing_period=BillingPeriod.MONTHLY,
    ),
)
```

Phase super evergreen

```python
super_evergreen = Phase(
    type=PhaseType.EVERGREEN,
    duration=Duration(time_unit=TimeUnit.UNLIMITED),
    recurring_price=RecurringPrice(
        prices=[Price("GBP", 750.00), Price("USD", 1000.00)],
        billing_period=BillingPeriod.MONTHLY,
    ),
)
```

Phase ADD-ON

```python
add_on_evergreen = Phase(
    type=PhaseType.EVERGREEN,
    duration=Duration(time_unit=TimeUnit.UNLIMITED),
    recurring_price=RecurringPrice(
        prices=[Price("GBP", 15.00), Price("USD", 20.00)],
        billing_period=BillingPeriod.MONTHLY,
    ),
)
```

Create rules (change and cancel rules are required)

```python
default_change_policy = ChangePolicyCase(policy=BillingPolicy.END_OF_TERM)

default_cancel_policy = CancelPolicyCase(policy=EntitlementPolicy.END_OF_TERM)

rules = Rules(
    change_policy_cases=[default_change_policy],
    cancel_policy_cases=[default_cancel_policy],
)
```

Create plans

```python
oil_slick_monthly = Plan(
    name="oil-slick-monthly",
    product=oil_slick,
    initial_phases=[],
    final_phase=add_on_evergreen,
)

remote_control_monthly = Plan(
    name="remote-control-monthly",
    product=remote_control,
    initial_phases=[],
    final_phase=add_on_evergreen,
)


standard_monthly = Plan(
    name="standard-monthly",
    product=standard,
    initial_phases=[phase_trial],
    final_phase=standard_evergreen,
)


sports_monthly = Plan(
    name="sports-monthly",
    product=sports,
    initial_phases=[phase_trial],
    final_phase=sports_evergreen,
)


super_monthly = Plan(
    name="super-monthly",
    product=super,
    initial_phases=[phase_trial],
    final_phase=super_evergreen,
)
```

Create catalog

```python
catalog = Catalog(
    name="SpyCarBasic",
    billing_mode=BillingMode.IN_ADVANCE,
    currencies=currencies,
    products=[standard, sports, super, oil_slick, remote_control],
    rules=rules,
    plans=[
        standard_monthly,
        sports_monthly,
        super_monthly,
        oil_slick_monthly,
        remote_control_monthly,
    ],
)
```

Get xml content

```python
print(catalog)
```

Save catalog as file

```python
catalog.write()
```

### TODO

#### Plans

- Usage
