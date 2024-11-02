from pydantic import Field

from datagarden_models.models.base import DataGardenModelLegends, DataGardenSubModel


class DemographicsBaseKeys:
	MALE = "male"
	FEMALE = "female"


class DemographicsBaseLegends(DataGardenModelLegends):
	AGE_GENDER_MALE = (
		"Number of males. " "In number of individuals per age or age group."
	)
	AGE_GENDER_FEMALE = (
		"Number of females. " "In number of individuals per age or age group."
	)


L = DemographicsBaseLegends


class AgeGender(DataGardenSubModel):
	male: dict = Field(default_factory=dict, description=L.AGE_GENDER_MALE)
	female: dict = Field(default_factory=dict, description=L.AGE_GENDER_FEMALE)
