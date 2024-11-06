from pydantic import Field

from ..base import DataGardenModel, DataGardenModelLegends
from .base_economics import EconomicBaseKeys
from .gdp import GDP, GDPV1Keys


class EconomicsV1Keys(GDPV1Keys, EconomicBaseKeys):
	GDP = "gdp"
	DATAGARDEN_MODEL_NAME = "Economics"


class EconomicsV1Legends(DataGardenModelLegends):
	GDP = "Gross Domestic Product"


L = EconomicsV1Legends


class EconomicsV1(DataGardenModel):
	MODEL_LEGEND: str = "Economic data for a region. "
	datagarden_model_version: str = Field(
		"v1.0", frozen=True, description=L.DATAGARDEN_MODEL_VERSION
	)
	gdp: GDP = Field(default_factory=GDP, description=L.GDP)
