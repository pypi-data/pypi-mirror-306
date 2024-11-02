from pydantic import BaseModel, Field


class HealthCareFacilitiesKeys:
	HOSPITAL_BEDS = "hospital_beds"


class HealthCareFacilitiesLegends:
	HOSPITAL_BEDS = "Number of hosital beds in region per 100.000 inhabitant"


L = HealthCareFacilitiesLegends


class HealthCareFacilities(BaseModel):
	hospital_beds: float | None = Field(default=None, description=L.HOSPITAL_BEDS)
