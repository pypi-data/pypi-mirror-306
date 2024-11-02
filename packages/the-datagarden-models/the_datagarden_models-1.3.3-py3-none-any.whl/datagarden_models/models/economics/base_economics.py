from pydantic import BaseModel, Field


class EconomicBaseKeys:
	VALUE = "value"
	UNIT = "unit"
	CURRENCY = "currency"


class EconomicBaseLegends:
	VALUE = "value in units of given currency,"
	UNIT = "units of measure."
	CURRENCY = "currency of measure."


L = EconomicBaseLegends


class EconomicsValue(BaseModel):
	value: float | None = Field(default=None, description=L.VALUE)
	unit: int = Field(default=1, description=L.UNIT)
	currency: str = Field(default="EUR", description=L.CURRENCY)


class EconomicsUnit(BaseModel):
	unit: int = Field(default=1, description=L.UNIT)
	currency: str = Field(default="EUR", description=L.CURRENCY)
