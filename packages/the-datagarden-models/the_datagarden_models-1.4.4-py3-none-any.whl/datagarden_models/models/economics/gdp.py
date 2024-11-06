from typing import Optional

from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel

from .base_economics import EconomicsUnit, EconomicsValue


class ValueAddedKeys:
	UNITS = "units"
	TOTAL = "total"
	BY_NACE_ACTIVIT = "by_nace_activity"


class ValueAddedLegends:
	TOTAL = "Total value added in given units."
	UNITS = "Currency and units."
	BY_NACE_ACTIVITY = (
		"By NACE economic activity. See also "
		"https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Statistical_classification_of_economic_activities_in_the_European_Community_(NACE)"
	)


LV = ValueAddedLegends


class ValueAdded(DataGardenSubModel):
	units: EconomicsUnit = Field(default_factory=EconomicsUnit, description=LV.UNITS)
	total: Optional[float] = Field(default=None, description=LV.TOTAL)
	by_nace_activity: dict = Field(
		default_factory=dict, description=LV.BY_NACE_ACTIVITY
	)


class GDPConstantLegends:
	TOTAL_GDP_CONSTANT_PRICES = "Total GDP at constant prices."
	GDP_PER_INHABITANT_CONSTANT_PRICES = "GDP per inhabitant at constant prices."
	REFERENCE_YEAR = "Reference year for the constant prices."


GC = GDPConstantLegends


class GDPConstantKeys:
	REFERENCE_YEAR = "reference_year"


class GDPAtConstantPrices(DataGardenSubModel):
	total_gdp: EconomicsValue = Field(
		default_factory=EconomicsValue, description=GC.TOTAL_GDP_CONSTANT_PRICES
	)
	gdp_per_inhabitant: EconomicsValue = Field(
		default_factory=EconomicsValue,
		description=GC.GDP_PER_INHABITANT_CONSTANT_PRICES,
	)
	reference_year: Optional[str] = Field(default=None, description=GC.REFERENCE_YEAR)


class GDPV1Legends:
	TOTAL_GDP = "Total GDP at current value for the region."
	GDP_PER_INHABITANT = "GDP per inhabitant current value."
	VALUE_ADDED = "Economic value added current value per region."
	GDP_AT_CONSTANT_PRICES = "GDP figures at constant prices."
	YOY_GROWTH = "Growth versus previous year in percent."
	YOY_GROWTH_PER_CAPITA = "Growth versus previous year in percent per capita."


L = GDPV1Legends


class GDP(DataGardenSubModel):
	total_gdp: EconomicsValue = Field(
		default_factory=EconomicsValue, description=L.TOTAL_GDP
	)
	gdp_per_inhabitant: EconomicsValue = Field(
		default_factory=EconomicsValue, description=L.GDP_PER_INHABITANT
	)
	value_added: ValueAdded = Field(default_factory=ValueAdded, description=L.TOTAL_GDP)
	gdp_at_constant_prices: GDPAtConstantPrices = Field(
		default_factory=GDPAtConstantPrices, description=L.GDP_AT_CONSTANT_PRICES
	)
	yoy_growth: Optional[float] = Field(default=None, description=L.YOY_GROWTH)
	yoy_growth_per_capita: Optional[float] = Field(
		default=None, description=L.YOY_GROWTH_PER_CAPITA
	)


class GDPV1Keys(ValueAddedKeys, GDPConstantKeys):
	TOTAL_GDP = "total_gdp"
	GDP_PER_INHABITANT = "gdp_per_inhabitant"
	VALUE_ADDED = "value_added"
	GDP_AT_CONSTANT_PRICES = "gdp_at_constant_prices"
	YOY_GROWTH = "yoy_growth"
	YOY_GROWTH_PER_CAPITA = "yoy_growth_per_capita"
