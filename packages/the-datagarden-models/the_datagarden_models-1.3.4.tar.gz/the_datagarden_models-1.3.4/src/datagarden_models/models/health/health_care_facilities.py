from pydantic import Field

from datagarden_models.models.base import DataGardenSubModel


class HealthCareFacilitiesKeys:
	HOSPITAL_BEDS = "hospital_beds"


class HealthCareFacilitiesLegends:
	HOSPITAL_BEDS = "Number of hosital beds in region per 100.000 inhabitant"


L = HealthCareFacilitiesLegends


class HealthCareFacilities(DataGardenSubModel):
	hospital_beds: float | None = Field(default=None, description=L.HOSPITAL_BEDS)
